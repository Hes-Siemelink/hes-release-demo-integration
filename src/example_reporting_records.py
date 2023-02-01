import datetime
import logging

from digitalai.release.container import BaseTask, BuildRecord, PlanRecord, \
    ItsmRecord, CodeComplianceRecord,DeploymentRecord

logger = logging.getLogger('Digitalai')


class ExampleReportingRecords(BaseTask):
    """
    Example class for adding various types of reporting records
    """
    def __init__(self, params):
        super().__init__()
        self.params = params

    def execute(self) -> None:
        """
        Executes the task for adding a reporting records to the OutputContext.
        """
        logger.debug(f"Task property values are  : {self.params}")
        try:
            value = self.params.get('inputValue')
            task_id = self.params.get('task_id')

            output_properties = self.get_output_properties()
            output_properties['outputValue'] = value

            build_record = BuildRecord(
                target_id=task_id,
                server_url="https://digital.ai",
                server_user="server user",
                build="build data",
                build_url="https://digital.ai",
                project="project 1",
                outcome="outcome data",
                start_date=datetime.datetime.now(),
                end_date=datetime.datetime.now(),
                duration="45s"
            )
            self.add_reporting_record(build_record)

            plan_record = PlanRecord(
                target_id=task_id,
                server_url="https://digital.ai",
                server_user="test user",
                ticket="1235",
                ticket_url="https://digital.ai",
                title="title 1",
                ticket_type="test type",
                status="success",
                updated_date=datetime.datetime.now(),
                updated_by="updated user"
            )
            self.add_reporting_record(plan_record)

            itsm_record = ItsmRecord(
                target_id=task_id,
                server_url="https://digital.ai",
                server_user="server user",
                record="1235",
                record_url="https://digital.ai",
                title="test title",
                status="success",
                priority="high",
                created_by="created user"
            )
            self.add_reporting_record(itsm_record)

            code_compliance_record = CodeComplianceRecord(
                target_id=task_id,
                server_url="https://digital.ai",
                server_user="server user",
                project="project 1",
                project_url="https://digital.ai",
                analysis_date=datetime.datetime.now(),
                outcome="outcome data",
                compliance_data="compliance data"
            )
            self.add_reporting_record(code_compliance_record)

            deployment_record = DeploymentRecord(
                target_id=task_id,
                server_url="https://digital.ai",
                server_user="server user",
                deployment_task="deployment task",
                deployment_task_url="https://digital.ai",
                application_name="application name",
                environment_name="environment name",
                version="version data",
                status="completed"
            )
            self.add_reporting_record(deployment_record)

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
