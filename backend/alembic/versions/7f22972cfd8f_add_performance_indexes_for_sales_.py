"""add_performance_indexes_for_sales_modules

Revision ID: 7f22972cfd8f
Revises: c039d407fbae
Create Date: 2025-09-23 14:45:24.549978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f22972cfd8f'
down_revision: Union[str, None] = 'c039d407fbae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add indexes for Lead table based on common query patterns
    op.create_index('ix_leads_status', 'leads', ['status'])
    op.create_index('ix_leads_source', 'leads', ['source'])
    op.create_index('ix_leads_assigned_to', 'leads', ['assigned_to'])
    op.create_index('ix_leads_created_at', 'leads', ['created_at'])
    op.create_index('ix_leads_value', 'leads', ['value'])
    
    # Add indexes for Contact table based on common query patterns
    op.create_index('ix_contacts_phone', 'contacts', ['phone'])
    op.create_index('ix_contacts_position', 'contacts', ['position'])
    op.create_index('ix_contacts_department', 'contacts', ['department'])
    op.create_index('ix_contacts_city', 'contacts', ['city'])
    op.create_index('ix_contacts_state', 'contacts', ['state'])
    op.create_index('ix_contacts_country', 'contacts', ['country'])
    
    # Add indexes for Opportunity table based on common query patterns
    op.create_index('ix_opportunities_account_id', 'opportunities', ['account_id'])
    op.create_index('ix_opportunities_contact_id', 'opportunities', ['contact_id'])
    op.create_index('ix_opportunities_stage', 'opportunities', ['stage'])
    op.create_index('ix_opportunities_assigned_to', 'opportunities', ['assigned_to'])
    op.create_index('ix_opportunities_value', 'opportunities', ['value'])
    op.create_index('ix_opportunities_probability', 'opportunities', ['probability'])
    op.create_index('ix_opportunities_close_date', 'opportunities', ['close_date'])
    op.create_index('ix_opportunities_created_at', 'opportunities', ['created_at'])
    
    # Add indexes for Quotation table based on common query patterns
    op.create_index('ix_quotations_opportunity_id', 'quotations', ['opportunity_id'])
    op.create_index('ix_quotations_account_id', 'quotations', ['account_id'])
    op.create_index('ix_quotations_contact_id', 'quotations', ['contact_id'])
    op.create_index('ix_quotations_status', 'quotations', ['status'])
    op.create_index('ix_quotations_amount', 'quotations', ['amount'])
    op.create_index('ix_quotations_total_amount', 'quotations', ['total_amount'])
    op.create_index('ix_quotations_valid_until', 'quotations', ['valid_until'])
    op.create_index('ix_quotations_created_at', 'quotations', ['created_at'])
    
    # Add indexes for Activity table based on common query patterns
    op.create_index('ix_activities_activity_type', 'activities', ['activity_type'])
    op.create_index('ix_activities_status', 'activities', ['status'])
    op.create_index('ix_activities_assigned_to', 'activities', ['assigned_to'])
    op.create_index('ix_activities_related_to', 'activities', ['related_to'])
    op.create_index('ix_activities_related_id', 'activities', ['related_id'])
    op.create_index('ix_activities_start_time', 'activities', ['start_time'])
    op.create_index('ix_activities_end_time', 'activities', ['end_time'])
    op.create_index('ix_activities_created_at', 'activities', ['created_at'])
    
    # Add indexes for Target table based on common query patterns
    op.create_index('ix_targets_target_type', 'targets', ['target_type'])
    op.create_index('ix_targets_period', 'targets', ['period'])
    op.create_index('ix_targets_year', 'targets', ['year'])
    op.create_index('ix_targets_assigned_to', 'targets', ['assigned_to'])
    op.create_index('ix_targets_target_value', 'targets', ['target_value'])
    op.create_index('ix_targets_created_at', 'targets', ['created_at'])
    
    # Add indexes for Report table based on common query patterns
    op.create_index('ix_reports_report_type', 'reports', ['report_type'])
    op.create_index('ix_reports_status', 'reports', ['status'])
    op.create_index('ix_reports_generated_by', 'reports', ['generated_by'])
    op.create_index('ix_reports_generated_at', 'reports', ['generated_at'])
    op.create_index('ix_reports_created_at', 'reports', ['created_at'])


def downgrade() -> None:
    # Drop indexes for Report table
    op.drop_index('ix_reports_created_at', table_name='reports')
    op.drop_index('ix_reports_generated_at', table_name='reports')
    op.drop_index('ix_reports_generated_by', table_name='reports')
    op.drop_index('ix_reports_status', table_name='reports')
    op.drop_index('ix_reports_report_type', table_name='reports')
    
    # Drop indexes for Target table
    op.drop_index('ix_targets_created_at', table_name='targets')
    op.drop_index('ix_targets_target_value', table_name='targets')
    op.drop_index('ix_targets_assigned_to', table_name='targets')
    op.drop_index('ix_targets_year', table_name='targets')
    op.drop_index('ix_targets_period', table_name='targets')
    op.drop_index('ix_targets_target_type', table_name='targets')
    
    # Drop indexes for Activity table
    op.drop_index('ix_activities_created_at', table_name='activities')
    op.drop_index('ix_activities_end_time', table_name='activities')
    op.drop_index('ix_activities_start_time', table_name='activities')
    op.drop_index('ix_activities_related_id', table_name='activities')
    op.drop_index('ix_activities_related_to', table_name='activities')
    op.drop_index('ix_activities_assigned_to', table_name='activities')
    op.drop_index('ix_activities_status', table_name='activities')
    op.drop_index('ix_activities_activity_type', table_name='activities')
    
    # Drop indexes for Quotation table
    op.drop_index('ix_quotations_created_at', table_name='quotations')
    op.drop_index('ix_quotations_valid_until', table_name='quotations')
    op.drop_index('ix_quotations_total_amount', table_name='quotations')
    op.drop_index('ix_quotations_amount', table_name='quotations')
    op.drop_index('ix_quotations_status', table_name='quotations')
    op.drop_index('ix_quotations_contact_id', table_name='quotations')
    op.drop_index('ix_quotations_account_id', table_name='quotations')
    op.drop_index('ix_quotations_opportunity_id', table_name='quotations')
    
    # Drop indexes for Opportunity table
    op.drop_index('ix_opportunities_created_at', table_name='opportunities')
    op.drop_index('ix_opportunities_close_date', table_name='opportunities')
    op.drop_index('ix_opportunities_probability', table_name='opportunities')
    op.drop_index('ix_opportunities_value', table_name='opportunities')
    op.drop_index('ix_opportunities_assigned_to', table_name='opportunities')
    op.drop_index('ix_opportunities_stage', table_name='opportunities')
    op.drop_index('ix_opportunities_contact_id', table_name='opportunities')
    op.drop_index('ix_opportunities_account_id', table_name='opportunities')
    
    # Drop indexes for Contact table
    op.drop_index('ix_contacts_country', table_name='contacts')
    op.drop_index('ix_contacts_state', table_name='contacts')
    op.drop_index('ix_contacts_city', table_name='contacts')
    op.drop_index('ix_contacts_department', table_name='contacts')
    op.drop_index('ix_contacts_position', table_name='contacts')
    op.drop_index('ix_contacts_phone', table_name='contacts')
    
    # Drop indexes for Lead table
    op.drop_index('ix_leads_value', table_name='leads')
    op.drop_index('ix_leads_created_at', table_name='leads')
    op.drop_index('ix_leads_assigned_to', table_name='leads')
    op.drop_index('ix_leads_source', table_name='leads')
    op.drop_index('ix_leads_status', table_name='leads')