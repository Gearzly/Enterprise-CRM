import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

interface ModulePageProps {
  title: string;
  description: string;
  module: string;
  submodule: string;
}

export function ModulePage({ title, description, module, submodule }: ModulePageProps) {
  const getModuleColor = (module: string) => {
    switch (module) {
      case 'sales': return 'bg-green-50 border-green-200 text-green-800';
      case 'marketing': return 'bg-blue-50 border-blue-200 text-blue-800';
      case 'support': return 'bg-purple-50 border-purple-200 text-purple-800';
      default: return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const moduleActions = {
    'sales/activities': [
      { label: 'New Activity', variant: 'default' as const },
      { label: 'View Calendar', variant: 'outline' as const },
      { label: 'Export Data', variant: 'outline' as const }
    ],
    'sales/contacts': [
      { label: 'Add Contact', variant: 'default' as const },
      { label: 'Import Contacts', variant: 'outline' as const },
      { label: 'Manage Groups', variant: 'outline' as const }
    ],
    'sales/leads': [
      { label: 'Create Lead', variant: 'default' as const },
      { label: 'Lead Scoring', variant: 'outline' as const },
      { label: 'Conversion Report', variant: 'outline' as const }
    ],
    'sales/opportunities': [
      { label: 'New Opportunity', variant: 'default' as const },
      { label: 'Pipeline View', variant: 'outline' as const },
      { label: 'Forecast', variant: 'outline' as const }
    ],
    'sales/quotations': [
      { label: 'Create Quote', variant: 'default' as const },
      { label: 'Templates', variant: 'outline' as const },
      { label: 'Approval Queue', variant: 'outline' as const }
    ],
    'sales/reports': [
      { label: 'Generate Report', variant: 'default' as const },
      { label: 'Scheduled Reports', variant: 'outline' as const },
      { label: 'Custom Dashboards', variant: 'outline' as const }
    ],
    'sales/targets': [
      { label: 'Set Targets', variant: 'default' as const },
      { label: 'Track Progress', variant: 'outline' as const },
      { label: 'Team Performance', variant: 'outline' as const }
    ],
    // Marketing actions
    'marketing/campaigns': [
      { label: 'New Campaign', variant: 'default' as const },
      { label: 'Templates', variant: 'outline' as const },
      { label: 'Performance Analytics', variant: 'outline' as const }
    ],
    'marketing/leads': [
      { label: 'Lead Capture', variant: 'default' as const },
      { label: 'Lead Nurturing', variant: 'outline' as const },
      { label: 'Qualification Rules', variant: 'outline' as const }
    ],
    'marketing/email': [
      { label: 'Create Email', variant: 'default' as const },
      { label: 'Email Templates', variant: 'outline' as const },
      { label: 'Delivery Reports', variant: 'outline' as const }
    ],
    // Support actions
    'support/tickets': [
      { label: 'New Ticket', variant: 'default' as const },
      { label: 'Ticket Queue', variant: 'outline' as const },
      { label: 'Escalation Rules', variant: 'outline' as const }
    ],
    'support/knowledge-base': [
      { label: 'Add Article', variant: 'default' as const },
      { label: 'Manage Categories', variant: 'outline' as const },
      { label: 'Usage Analytics', variant: 'outline' as const }
    ],
    'support/live-chat': [
      { label: 'Start Chat Session', variant: 'default' as const },
      { label: 'Chat History', variant: 'outline' as const },
      { label: 'Agent Performance', variant: 'outline' as const }
    ]
  };

  const currentActions = moduleActions[`${module}/${submodule}` as keyof typeof moduleActions] || [
    { label: 'Create New', variant: 'default' as const },
    { label: 'View All', variant: 'outline' as const },
    { label: 'Settings', variant: 'outline' as const }
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Badge className={getModuleColor(module)}>
              {module.charAt(0).toUpperCase() + module.slice(1)}
            </Badge>
            <span className="text-muted-foreground">•</span>
            <span className="text-muted-foreground capitalize">{submodule.replace('-', ' ')}</span>
          </div>
          <h1 className="text-2xl font-semibold">{title}</h1>
          <p className="text-muted-foreground">{description}</p>
        </div>
        
        <div className="flex gap-2">
          {currentActions.map((action, index) => (
            <Button key={index} variant={action.variant}>
              {action.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {Array.from({ length: 4 }, (_, i) => (
          <Card key={i} className="p-4">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">
                {i === 0 ? 'Total' : i === 1 ? 'Active' : i === 2 ? 'Pending' : 'Completed'}
              </p>
              <p className="text-2xl font-semibold">
                {i === 0 ? '2,847' : i === 1 ? '156' : i === 2 ? '43' : '2,648'}
              </p>
              <p className="text-xs text-muted-foreground">
                {i % 2 === 0 ? '+12% from last month' : '-5% from last week'}
              </p>
            </div>
          </Card>
        ))}
      </div>

      {/* Main Content Area */}
      <Card className="p-8">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto">
            <div className="w-8 h-8 bg-primary/20 rounded-full"></div>
          </div>
          <div>
            <h3 className="text-lg font-semibold">{title} Management</h3>
            <p className="text-muted-foreground mt-2">
              This {submodule.replace('-', ' ')} management interface would contain detailed functionality for managing {submodule.replace('-', ' ')} in your {module} workflow.
            </p>
          </div>
          <div className="flex justify-center gap-3 pt-4">
            <Button>Get Started</Button>
            <Button variant="outline">Learn More</Button>
          </div>
        </div>
      </Card>

      {/* Feature List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[
          'Advanced Filtering',
          'Bulk Operations',
          'Export/Import',
          'Automated Workflows',
          'Real-time Updates',
          'Integration APIs'
        ].map((feature, index) => (
          <Card key={index} className="p-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                <div className="w-4 h-4 bg-primary/30 rounded"></div>
              </div>
              <div>
                <p className="font-medium">{feature}</p>
                <p className="text-sm text-muted-foreground">Available in this module</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}