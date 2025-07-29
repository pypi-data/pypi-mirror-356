"""Parser module to parse gear config.json."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import flywheel
from fw_classification.classify import Profile
from fw_classification.classify.block import Block
from fw_gear import GearContext as GearToolkitContext

log = logging.getLogger(__name__)

default_profiles = (Path(__file__).parents[0] / "classification_profiles").resolve()


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[
    Dict[str, Any], Profile, bool, bool
]:  # File input  # Profile to classify with
    """Parse options from gear config.

    Args:
        gear_context (GearToolkitContext): Gear toolkit context.

    Returns:
        tuple:
            - File input as a dictionary
            - Profile to use for classification, defaults to the
                classification-toolkits "main.yml"
            - Whether to validate classification schema
            - Whether to remove existing classification
    """
    file_input: Dict[str, Any] = gear_context.config.get_input("file-input")

    validate = gear_context.config.opts.get("validate")

    remove_existing = gear_context.config.opts.get("remove_existing")

    # Get optional custom profile from input
    profile_path: Optional[Path] = gear_context.config.get_input_path("profile")

    if profile_path:
        log.info("Using profile from input '%s'", profile_path)
        profile = Profile(profile_path, include_search_dirs=[default_profiles])
    else:
        # Default to the classification-profile's "main.yaml" which should
        #   be a "catch-all" and is defined in the fw-classification-profiles
        #   repo under classification_profiles/main.yaml
        log.info("Using default profile 'main.yaml'")
        profile = Profile(default_profiles / "main.yaml")

    # Get optional custom classifications from project context
    project = get_parent_project(gear_context)
    log.info("Looking for custom classifications in project %s", project.label)
    classify_context = project.get("info", {}).get("classifications", {})
    custom_block = None
    if classify_context:
        log.debug("Context classification: %s", classify_context)
        try:
            block = {"name": "custom", "rules": classify_context}
            custom_block, err = Block.from_dict(block)
            if err:
                log.error("\n".join([str(e) for e in err]))
                raise RuntimeError()
            log.info(
                "Found custom classification in project context, parsed as:\n%s",
                custom_block,
            )
            # Add custom block to the end of the profile if it's defined.
            profile.handle_block(custom_block, "custom")  # type: ignore
        except:  # noqa: E722
            log.warning("Could not handle context classification %s", classify_context)

    return file_input, profile, validate, remove_existing


def get_parent_project(context: GearToolkitContext) -> flywheel.models.Project:
    """Returns parent project"""
    dst = context.config.get_destination_container()
    return context.client.get_project(dst.parents.project)
