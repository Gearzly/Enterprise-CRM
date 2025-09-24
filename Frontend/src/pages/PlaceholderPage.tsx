import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Construction, ArrowLeft, Settings, Plus } from 'lucide-react';

interface PlaceholderPageProps {
  title: string;
  description: string;
  module: string;
  submodule: string;
}

export function PlaceholderPage({ title, description, module, submodule }: PlaceholderPageProps) {
  const getModuleColor = (module: string) => {
    switch (module) {
      case 'sales': return 'bg-green-50 border-green-200 text-green-800';
      case 'marketing': return 'bg-blue-50 border-blue-200 text-blue-800';
      case 'support': return 'bg-purple-50 border-purple-200 text-purple-800';
      case 'admin': return 'bg-gray-50 border-gray-200 text-gray-800';
      default: return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getSampleFeatures = (module: string, submodule: string) => {
    const baseFeatures = [
      'Advanced filtering and search',
      'Real-time updates and notifications', 
      'Bulk operations and mass actions',
      'Export and import functionality',
      'Custom fields and workflows',
      'Integration with external tools',
      'Automated reporting and analytics',
      'Role-based permissions',
      'Audit trail and activity logging',
      'Mobile responsive interface'
    ];

    const moduleSpecificFeatures = {
      'sales/reports': [
        'Interactive dashboards',
        'Scheduled report delivery',
        'Custom report builder',
        'KPI tracking and alerts'
      ],
      'sales/targets': [
        'Goal setting and tracking',
        'Performance comparisons',
        'Achievement tracking',
        'Incentive calculations'
      ],
      'marketing/email': [
        'Email template builder',
        'A/B testing capabilities',
        'Delivery optimization',
        'Subscriber management'
      ],
      'marketing/social-media': [
        'Multi-platform posting',
        'Content scheduling',
        'Engagement analytics',
        'Social listening tools'
      ],
      'marketing/automation': [
        'Workflow builder',
        'Trigger-based actions',
        'Lead scoring automation',
        'Nurture campaigns'
      ],
      'support/knowledge-base': [
        'Article management',
        'Category organization',
        'Search functionality',
        'Usage analytics'
      ],
      'support/live-chat': [
        'Real-time messaging',
        'Chat routing',
        'Canned responses',
        'Chat transcripts'
      ],
      'support/sla': [
        'SLA definition and tracking',
        'Escalation rules',
        'Performance monitoring',
        'Compliance reporting'
      ]
    };

    const specific = moduleSpecificFeatures[`${module}/${submodule}` as keyof typeof moduleSpecificFeatures] || [];
    return [...specific.slice(0, 4), ...baseFeatures.slice(0, 6)];
  };

  const getSampleMetrics = (module: string, submodule: string) => {
    const baseMetrics = [
      { label: 'Total Records', value: '2,847', change: '+12%' },
      { label: 'Active Items', value: '156', change: '+8%' },
      { label: 'This Month', value: '43', change: '+15%' },
      { label: 'Completion Rate', value: '94%', change: '+3%' }
    ];

    // Customize metrics based on module/submodule
    const customizations = {
      'sales': { 
        labels: ['Total Sales', 'Active Deals', 'This Month', 'Close Rate'],
        colors: ['text-green-600', 'text-blue-600', 'text-purple-600', 'text-orange-600']
      },
      'marketing': {
        labels: ['Total Campaigns', 'Active Campaigns', 'This Month', 'Success Rate'],
        colors: ['text-blue-600', 'text-green-600', 'text-purple-600', 'text-orange-600']
      },
      'support': {
        labels: ['Total Tickets', 'Open Tickets', 'Resolved Today', 'Satisfaction'],
        colors: ['text-purple-600', 'text-orange-600', 'text-green-600', 'text-blue-600']
      }
    };

    const custom = customizations[module as keyof typeof customizations];
    if (custom) {
      return baseMetrics.map((metric, index) => ({
        ...metric,
        label: custom.labels[index] || metric.label,
        color: custom.colors[index] || 'text-gray-600'
      }));
    }

    return baseMetrics.map(metric => ({ ...metric, color: 'text-gray-600' }));
  };

  const features = getSampleFeatures(module, submodule);
  const metrics = getSampleMetrics(module, submodule);

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
          <Button variant="outline">
            <Settings className="w-4 h-4 mr-2" />
            Configure
          </Button>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Create New
          </Button>
        </div>
      </div>

      {/* Quick Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {metrics.map((metric, index) => (
          <Card key={index} className="p-4">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{metric.label}</p>
              <p className="text-2xl font-semibold">{metric.value}</p>
              <p className={`text-xs ${metric.color}`}>{metric.change} from last period</p>
            </div>
          </Card>
        ))}
      </div>

      {/* Coming Soon Section */}
      <Card className="p-8">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto">
            <Construction className="w-8 h-8 text-muted-foreground" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Page Under Development</h3>
            <p className="text-muted-foreground mt-2 max-w-md mx-auto">
              This {submodule.replace('-', ' ')} management interface is currently being developed. 
              Check back soon for the full functionality!
            </p>
          </div>
          <div className="flex justify-center gap-3 pt-4">
            <Button variant="outline">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Go Back
            </Button>
            <Button variant="outline">Get Notified</Button>
          </div>
        </div>
      </Card>

      {/* Planned Features */}
      <Card className="p-6">
        <h3 className="font-semibold mb-4">Planned Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {features.map((feature, index) => (
            <div key={index} className="flex items-center gap-3 p-3 bg-muted rounded-lg">
              <div className="w-2 h-2 bg-primary rounded-full"></div>
              <span className="text-sm">{feature}</span>
            </div>
          ))}
        </div>
      </Card>

      {/* Module Info */}
      <Card className="p-6">
        <h3 className="font-semibold mb-4">Module Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 className="font-medium mb-2">Integration Points</h4>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Customer Management</li>
              <li>• Activity Tracking</li>
              <li>• Reporting System</li>
              <li>• Notification Center</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium mb-2">Data Sources</h4>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• CRM Database</li>
              <li>• External APIs</li>
              <li>• User Interactions</li>
              <li>• System Events</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium mb-2">Access Levels</h4>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Admin: Full Access</li>
              <li>• Manager: Read/Write</li>
              <li>• User: Limited Access</li>
              <li>• Guest: View Only</li>
            </ul>
          </div>
        </div>
      </Card>
    </div>
  );
}