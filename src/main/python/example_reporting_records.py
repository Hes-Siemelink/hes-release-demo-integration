import datetime
import logging
from dai_release_sdk import BaseTask, BuildRecord, PlanRecord, ItsmRecord, CodeComplianceRecord, DeploymentRecord

logger = logging.getLogger('DAI')


class ExampleReportingRecords(BaseTask):

    def __init__(self, params):
        super().__init__()
        self.params = params

    def execute(self) -> None:
        logger.debug(f"Task property values are  : {self.params}")
        try:
            value = self.params['inputValue']

            output_properties = self.get_output_properties()
            output_properties['outputValue'] = value
            reporting_records = self.get_reporting_records()

            build_record = BuildRecord(
                target_id=self.params['task_id'],
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
            reporting_records.append(build_record)

            plan_record = PlanRecord(
                target_id=self.params['task_id'],
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
            reporting_records.append(plan_record)

            itsm_record = ItsmRecord(
                target_id=self.params['task_id'],
                server_url="https://digital.ai",
                server_user="server user",
                record="1235",
                record_url="https://digital.ai",
                title="test title",
                status="success",
                priority="high",
                created_by="created user"
            )
            reporting_records.append(itsm_record)

            code_compliance_record = CodeComplianceRecord(
                target_id=self.params['task_id'],
                server_url="https://digital.ai",
                server_user="server user",
                project="project 1",
                project_url="https://digital.ai",
                analysis_date=datetime.datetime.now(),
                outcome="outcome data",
                compliance_data="compliance data"
            )
            reporting_records.append(code_compliance_record)

            deployment_record = DeploymentRecord(
                target_id=self.params['task_id'],
                server_url="https://digital.ai",
                server_user="server user",
                deployment_task="deployment task",
                deployment_task_url="https://digital.ai",
                application_name="application name",
                environment_name="environment name",
                version="version data",
                status="completed"
            )
            reporting_records.append(deployment_record)

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
