from bioblend.galaxy.objects import wrappers
from django.db import models

from .history import History
from .invocation import Invocation
from .galaxy_element import GalaxyElement

from django_to_galaxy.utils import load_galaxy_invocation_time_to_datetime


class Workflow(GalaxyElement):
    """Table for Galaxy workflows."""

    galaxy_owner = models.ForeignKey(
        "GalaxyUser", null=False, on_delete=models.CASCADE, related_name="workflows"
    )
    """Galaxy user that owns the workflow."""
    _step_jobs_count = models.PositiveIntegerField(default=0)
    """Number of step jobs of the workflow."""
    _is_meta = models.BooleanField(null=True, default=None, blank=True)
    """Indicates whether the workflow is a meta (i.e., has sub-workflows) or not."""

    @property
    def galaxy_workflow(self) -> wrappers.Workflow:
        """Galaxy object using bioblend."""
        if getattr(self, "_galaxy_workflow", None) is None:
            self._galaxy_workflow = self._get_galaxy_workflow()
        return self._galaxy_workflow

    def _get_galaxy_workflow(self) -> wrappers.Workflow:
        """Get galaxy object using bioblend."""
        return self.galaxy_owner.obj_gi.workflows.get(self.galaxy_id)

    def get_is_meta(self):
        """Sets / returns _is_meta value."""
        if self._is_meta is None:
            self._is_meta = False
            for key, step_dict in self.galaxy_workflow.steps.items():
                w = step_dict.wrapped
                if "workflow_id" in w:
                    self._is_meta = True
                    break
            self.save(update_fields=["_is_meta"])
        return self._is_meta

    def get_step_jobs_count(self):
        """Sets / returns _step_jobs_count value."""
        if self._step_jobs_count == 0:
            galaxy_wf = self.galaxy_workflow
            step_jobs_count = 0
            if self.get_is_meta():
                # Total step jobs count for a meta wf
                galaxy_client = self.galaxy_owner.obj_gi.gi
                for key, step_dict in galaxy_wf.steps.items():
                    w = step_dict.wrapped
                    if "workflow_id" in w:
                        sub_wf = galaxy_client.make_get_request(
                            galaxy_client.base_url
                            + f"/api/workflows/{w['workflow_id']}",
                            params={"instance": "true"},
                        ).json()
                        for j in range(len(sub_wf["steps"])):
                            step = sub_wf["steps"][str(j)]
                            if "input" not in step["type"]:
                                step_jobs_count += 1
            else:
                # Total step jobs count for a simple wf
                for key, step_dict in galaxy_wf.steps.items():
                    w = step_dict.wrapped
                    if "input" not in w["type"]:
                        step_jobs_count += 1
            self._step_jobs_count = step_jobs_count
            self.save(update_fields=["_step_jobs_count"])
        return self._step_jobs_count

    def invoke(self, datamap: dict, history: History) -> wrappers.Invocation:
        """
        Invoke workflow using bioblend.

        Args:
            datamap: dictionnary to link dataset to workflow inputs
            history: history obj the dataset(s) come from

        Returns:
            Invocation object from bioblend
        """
        galaxy_inv = self.galaxy_workflow.invoke(
            datamap, history=history.galaxy_history
        )
        # Create invocations
        invocation = Invocation(
            galaxy_id=galaxy_inv.id,
            galaxy_state=galaxy_inv.state,
            workflow=self,
            history=history,
            create_time=load_galaxy_invocation_time_to_datetime(galaxy_inv),
        )
        invocation.save()
        # Create output files
        invocation.create_output_files()
        return invocation

    def __repr__(self):
        return f"Workflow: {super().__str__()}"
