import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import {
  Database,
  Users,
  TrendingUp,
  Activity,
  Search,
  Filter,
  Plus,
  Download,
  Upload,
  Settings,
  Eye,
  Edit,
  Trash2,
  RefreshCw,
  BarChart3,
  PieChart,
  LineChart,
  Globe,
  Smartphone,
  Mail,
  ShoppingCart,
  Calendar,
  MapPin,
  DollarSign,
  Clock,
  Target,
  Zap,
  Link,
  CheckCircle,
  AlertCircle,
  XCircle,
  Info,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
} from 'lucide-react';

// Interfaces
interface DataSource {
  id: string;
  name: string;
  type: 'CRM' | 'E-commerce' | 'Social Media' | 'Email' | 'Website' | 'Mobile App' | 'Survey' | 'Third Party';
  status: 'Connected' | 'Disconnected' | 'Syncing' | 'Error';
  lastSync: string;
  recordCount: number;
  dataQuality: number;
}

interface CustomerProfile {
  id: string;
  name: string;
  email: string;
  phone: string;
  segment: string;
  lifetimeValue: number;
  lastActivity: string;
  engagementScore: number;
  preferredChannel: string;
  location: string;
  tags: string[];
}

interface Insight {
  id: string;
  title: string;
  description: string;
  type: 'Trend' | 'Anomaly' | 'Opportunity' | 'Risk';
  impact: 'High' | 'Medium' | 'Low';
  confidence: number;
  createdAt: string;
  metrics: {
    value: number;
    change: number;
    unit: string;
  };
}

interface Journey {
  id: string;
  name: string;
  description: string;
  stages: string[];
  customerCount: number;
  conversionRate: number;
  avgDuration: string;
  status: 'Active' | 'Draft' | 'Paused';
}

const CDPPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [activeTab, setActiveTab] = useState('overview');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isIntegrationDialogOpen, setIsIntegrationDialogOpen] = useState(false);

  // Mock data
  const dataSources: DataSource[] = [
    {
      id: '1',
      name: 'Salesforce CRM',
      type: 'CRM',
      status: 'Connected',
      lastSync: '2024-01-15 10:30 AM',
      recordCount: 15420,
      dataQuality: 95,
    },
    {
      id: '2',
      name: 'Shopify Store',
      type: 'E-commerce',
      status: 'Connected',
      lastSync: '2024-01-15 10:25 AM',
      recordCount: 8750,
      dataQuality: 88,
    },
    {
      id: '3',
      name: 'Facebook Ads',
      type: 'Social Media',
      status: 'Syncing',
      lastSync: '2024-01-15 09:45 AM',
      recordCount: 12300,
      dataQuality: 82,
    },
    {
      id: '4',
      name: 'Mailchimp',
      type: 'Email',
      status: 'Connected',
      lastSync: '2024-01-15 10:15 AM',
      recordCount: 25600,
      dataQuality: 91,
    },
    {
      id: '5',
      name: 'Google Analytics',
      type: 'Website',
      status: 'Error',
      lastSync: '2024-01-14 11:20 PM',
      recordCount: 45200,
      dataQuality: 76,
    },
  ];

  const customerProfiles: CustomerProfile[] = [
    {
      id: '1',
      name: 'Sarah Johnson',
      email: 'sarah.johnson@email.com',
      phone: '+1 (555) 123-4567',
      segment: 'High Value',
      lifetimeValue: 15420,
      lastActivity: '2024-01-15',
      engagementScore: 92,
      preferredChannel: 'Email',
      location: 'New York, NY',
      tags: ['VIP', 'Frequent Buyer', 'Email Subscriber'],
    },
    {
      id: '2',
      name: 'Michael Chen',
      email: 'michael.chen@email.com',
      phone: '+1 (555) 234-5678',
      segment: 'Growing',
      lifetimeValue: 8750,
      lastActivity: '2024-01-14',
      engagementScore: 78,
      preferredChannel: 'SMS',
      location: 'San Francisco, CA',
      tags: ['Tech Enthusiast', 'Mobile User'],
    },
    {
      id: '3',
      name: 'Emily Rodriguez',
      email: 'emily.rodriguez@email.com',
      phone: '+1 (555) 345-6789',
      segment: 'At Risk',
      lifetimeValue: 3200,
      lastActivity: '2024-01-10',
      engagementScore: 45,
      preferredChannel: 'Social Media',
      location: 'Austin, TX',
      tags: ['Inactive', 'Social Media'],
    },
  ];

  const insights: Insight[] = [
    {
      id: '1',
      title: 'Customer Churn Risk Increasing',
      description: 'Identified 15% increase in customers showing churn indicators in the past 30 days.',
      type: 'Risk',
      impact: 'High',
      confidence: 87,
      createdAt: '2024-01-15',
      metrics: { value: 15, change: 5, unit: '%' },
    },
    {
      id: '2',
      title: 'Mobile Engagement Surge',
      description: 'Mobile app engagement has increased by 32% among millennials.',
      type: 'Opportunity',
      impact: 'Medium',
      confidence: 94,
      createdAt: '2024-01-14',
      metrics: { value: 32, change: 12, unit: '%' },
    },
    {
      id: '3',
      title: 'Email Campaign Performance Drop',
      description: 'Open rates for email campaigns have decreased by 8% this month.',
      type: 'Anomaly',
      impact: 'Medium',
      confidence: 76,
      createdAt: '2024-01-13',
      metrics: { value: 8, change: -3, unit: '%' },
    },
  ];

  const journeys: Journey[] = [
    {
      id: '1',
      name: 'New Customer Onboarding',
      description: 'Complete onboarding journey for new customers',
      stages: ['Welcome', 'Profile Setup', 'First Purchase', 'Follow-up'],
      customerCount: 1250,
      conversionRate: 68,
      avgDuration: '7 days',
      status: 'Active',
    },
    {
      id: '2',
      name: 'Win-Back Campaign',
      description: 'Re-engage inactive customers',
      stages: ['Identification', 'Email Outreach', 'Incentive Offer', 'Conversion'],
      customerCount: 890,
      conversionRate: 23,
      avgDuration: '14 days',
      status: 'Active',
    },
    {
      id: '3',
      name: 'VIP Customer Experience',
      description: 'Premium experience for high-value customers',
      stages: ['Recognition', 'Exclusive Access', 'Personal Service', 'Loyalty Rewards'],
      customerCount: 156,
      conversionRate: 89,
      avgDuration: '30 days',
      status: 'Draft',
    },
  ];

  // Helper functions
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Connected':
        return 'bg-green-100 text-green-800';
      case 'Syncing':
        return 'bg-blue-100 text-blue-800';
      case 'Error':
        return 'bg-red-100 text-red-800';
      case 'Disconnected':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'CRM':
        return <Database className="h-4 w-4" />;
      case 'E-commerce':
        return <ShoppingCart className="h-4 w-4" />;
      case 'Social Media':
        return <Globe className="h-4 w-4" />;
      case 'Email':
        return <Mail className="h-4 w-4" />;
      case 'Website':
        return <Globe className="h-4 w-4" />;
      case 'Mobile App':
        return <Smartphone className="h-4 w-4" />;
      default:
        return <Database className="h-4 w-4" />;
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'Trend':
        return <TrendingUp className="h-4 w-4" />;
      case 'Anomaly':
        return <AlertCircle className="h-4 w-4" />;
      case 'Opportunity':
        return <Target className="h-4 w-4" />;
      case 'Risk':
        return <XCircle className="h-4 w-4" />;
      default:
        return <Info className="h-4 w-4" />;
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'High':
        return 'bg-red-100 text-red-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'Low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSegmentColor = (segment: string) => {
    switch (segment) {
      case 'High Value':
        return 'bg-purple-100 text-purple-800';
      case 'Growing':
        return 'bg-blue-100 text-blue-800';
      case 'At Risk':
        return 'bg-red-100 text-red-800';
      case 'New':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Create Integration Dialog Component
  const CreateIntegrationDialog = () => (
    <Dialog open={isIntegrationDialogOpen} onOpenChange={setIsIntegrationDialogOpen}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Add Data Source</DialogTitle>
          <DialogDescription>
            Connect a new data source to your Customer Data Platform.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <Label htmlFor="source-name">Source Name</Label>
            <Input id="source-name" placeholder="Enter source name" />
          </div>
          <div>
            <Label htmlFor="source-type">Source Type</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select source type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="crm">CRM</SelectItem>
                <SelectItem value="ecommerce">E-commerce</SelectItem>
                <SelectItem value="social">Social Media</SelectItem>
                <SelectItem value="email">Email</SelectItem>
                <SelectItem value="website">Website</SelectItem>
                <SelectItem value="mobile">Mobile App</SelectItem>
                <SelectItem value="survey">Survey</SelectItem>
                <SelectItem value="third-party">Third Party</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="connection-string">Connection Details</Label>
            <Textarea
              id="connection-string"
              placeholder="Enter connection details or API credentials"
              rows={3}
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsIntegrationDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsIntegrationDialogOpen(false)}>
            Connect Source
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Customer Data Platform</h1>
          <p className="text-gray-600 mt-1">
            Unified customer data, insights, and journey orchestration
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export Data
          </Button>
          <Button size="sm" onClick={() => setIsIntegrationDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Data Source
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Customers</p>
                <p className="text-2xl font-bold">127,543</p>
                <p className="text-xs text-green-600 flex items-center mt-1">
                  <ArrowUpRight className="h-3 w-3 mr-1" />
                  +12.5% from last month
                </p>
              </div>
              <Users className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Data Sources</p>
                <p className="text-2xl font-bold">12</p>
                <p className="text-xs text-blue-600 flex items-center mt-1">
                  <RefreshCw className="h-3 w-3 mr-1" />
                  5 syncing now
                </p>
              </div>
              <Database className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Data Quality</p>
                <p className="text-2xl font-bold">87%</p>
                <p className="text-xs text-yellow-600 flex items-center mt-1">
                  <Minus className="h-3 w-3 mr-1" />
                  -2% from last week
                </p>
              </div>
              <Activity className="h-8 w-8 text-yellow-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Journeys</p>
                <p className="text-2xl font-bold">8</p>
                <p className="text-xs text-green-600 flex items-center mt-1">
                  <ArrowUpRight className="h-3 w-3 mr-1" />
                  +3 this month
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="data-sources">Data Sources</TabsTrigger>
          <TabsTrigger value="customers">Customer Profiles</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
          <TabsTrigger value="journeys">Customer Journeys</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Data Quality Overview */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Data Quality Overview
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {dataSources.slice(0, 3).map((source) => (
                  <div key={source.id} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>{source.name}</span>
                      <span>{source.dataQuality}%</span>
                    </div>
                    <Progress value={source.dataQuality} className="h-2" />
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Recent Insights */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  Recent AI Insights
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {insights.slice(0, 3).map((insight) => (
                  <div key={insight.id} className="flex items-start gap-3 p-3 border rounded-lg">
                    <div className="mt-1">{getInsightIcon(insight.type)}</div>
                    <div className="flex-1">
                      <h4 className="font-medium text-sm">{insight.title}</h4>
                      <p className="text-xs text-gray-600 mt-1">{insight.description}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant="secondary" className={getImpactColor(insight.impact)}>
                          {insight.impact} Impact
                        </Badge>
                        <span className="text-xs text-gray-500">{insight.confidence}% confidence</span>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Customer Segments Distribution */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <PieChart className="h-5 w-5" />
                Customer Segments Distribution
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 border rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">35%</div>
                  <div className="text-sm text-gray-600">High Value</div>
                  <div className="text-xs text-gray-500">44,640 customers</div>
                </div>
                <div className="text-center p-4 border rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">28%</div>
                  <div className="text-sm text-gray-600">Growing</div>
                  <div className="text-xs text-gray-500">35,712 customers</div>
                </div>
                <div className="text-center p-4 border rounded-lg">
                  <div className="text-2xl font-bold text-green-600">22%</div>
                  <div className="text-sm text-gray-600">New</div>
                  <div className="text-xs text-gray-500">28,059 customers</div>
                </div>
                <div className="text-center p-4 border rounded-lg">
                  <div className="text-2xl font-bold text-red-600">15%</div>
                  <div className="text-sm text-gray-600">At Risk</div>
                  <div className="text-xs text-gray-500">19,132 customers</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Data Sources Tab */}
        <TabsContent value="data-sources" className="space-y-6">
          <div className="flex justify-between items-center">
            <div className="flex gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  placeholder="Search data sources..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              <Select value={selectedFilter} onValueChange={setSelectedFilter}>
                <SelectTrigger className="w-40">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Sources</SelectItem>
                  <SelectItem value="connected">Connected</SelectItem>
                  <SelectItem value="error">Error</SelectItem>
                  <SelectItem value="syncing">Syncing</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button onClick={() => setIsIntegrationDialogOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Data Source
            </Button>
          </div>

          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Source</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Last Sync</TableHead>
                  <TableHead>Records</TableHead>
                  <TableHead>Data Quality</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {dataSources.map((source) => (
                  <TableRow key={source.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        {getTypeIcon(source.type)}
                        <span className="font-medium">{source.name}</span>
                      </div>
                    </TableCell>
                    <TableCell>{source.type}</TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(source.status)}>
                        {source.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-gray-600">{source.lastSync}</TableCell>
                    <TableCell>{source.recordCount.toLocaleString()}</TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Progress value={source.dataQuality} className="w-16 h-2" />
                        <span className="text-sm">{source.dataQuality}%</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <Button variant="ghost" size="sm">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Settings className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <RefreshCw className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        </TabsContent>

        {/* Customer Profiles Tab */}
        <TabsContent value="customers" className="space-y-6">
          <div className="flex justify-between items-center">
            <div className="flex gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  placeholder="Search customers..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              <Select value={selectedFilter} onValueChange={setSelectedFilter}>
                <SelectTrigger className="w-40">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Segments</SelectItem>
                  <SelectItem value="high-value">High Value</SelectItem>
                  <SelectItem value="growing">Growing</SelectItem>
                  <SelectItem value="at-risk">At Risk</SelectItem>
                  <SelectItem value="new">New</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button>
              <Download className="h-4 w-4 mr-2" />
              Export Profiles
            </Button>
          </div>

          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Customer</TableHead>
                  <TableHead>Segment</TableHead>
                  <TableHead>Lifetime Value</TableHead>
                  <TableHead>Engagement Score</TableHead>
                  <TableHead>Last Activity</TableHead>
                  <TableHead>Preferred Channel</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {customerProfiles.map((customer) => (
                  <TableRow key={customer.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{customer.name}</div>
                        <div className="text-sm text-gray-600">{customer.email}</div>
                        <div className="text-xs text-gray-500 flex items-center gap-1 mt-1">
                          <MapPin className="h-3 w-3" />
                          {customer.location}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getSegmentColor(customer.segment)}>
                        {customer.segment}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <DollarSign className="h-4 w-4 text-green-600" />
                        {customer.lifetimeValue.toLocaleString()}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Progress value={customer.engagementScore} className="w-16 h-2" />
                        <span className="text-sm">{customer.engagementScore}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-sm text-gray-600">{customer.lastActivity}</TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        {customer.preferredChannel === 'Email' && <Mail className="h-4 w-4" />}
                        {customer.preferredChannel === 'SMS' && <Smartphone className="h-4 w-4" />}
                        {customer.preferredChannel === 'Social Media' && <Globe className="h-4 w-4" />}
                        <span className="text-sm">{customer.preferredChannel}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <Button variant="ghost" size="sm">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Edit className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="insights" className="space-y-6">
          <div className="flex justify-between items-center">
            <div className="flex gap-4">
              <Select value={selectedFilter} onValueChange={setSelectedFilter}>
                <SelectTrigger className="w-40">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Insights</SelectItem>
                  <SelectItem value="trend">Trends</SelectItem>
                  <SelectItem value="anomaly">Anomalies</SelectItem>
                  <SelectItem value="opportunity">Opportunities</SelectItem>
                  <SelectItem value="risk">Risks</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button>
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh Insights
            </Button>
          </div>

          <div className="grid gap-6">
            {insights.map((insight) => (
              <Card key={insight.id}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="p-2 rounded-lg bg-gray-100">
                        {getInsightIcon(insight.type)}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold">{insight.title}</h3>
                          <Badge className={getImpactColor(insight.impact)}>
                            {insight.impact} Impact
                          </Badge>
                        </div>
                        <p className="text-gray-600 mb-3">{insight.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <span>Confidence: {insight.confidence}%</span>
                          <span>•</span>
                          <span>{insight.createdAt}</span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold flex items-center gap-1">
                        {insight.metrics.change > 0 ? (
                          <ArrowUpRight className="h-5 w-5 text-green-600" />
                        ) : insight.metrics.change < 0 ? (
                          <ArrowDownRight className="h-5 w-5 text-red-600" />
                        ) : (
                          <Minus className="h-5 w-5 text-gray-600" />
                        )}
                        {insight.metrics.value}{insight.metrics.unit}
                      </div>
                      <div className="text-sm text-gray-500">
                        {insight.metrics.change > 0 ? '+' : ''}{insight.metrics.change}{insight.metrics.unit} change
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Customer Journeys Tab */}
        <TabsContent value="journeys" className="space-y-6">
          <div className="flex justify-between items-center">
            <div className="flex gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  placeholder="Search journeys..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              <Select value={selectedFilter} onValueChange={setSelectedFilter}>
                <SelectTrigger className="w-40">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Journeys</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="draft">Draft</SelectItem>
                  <SelectItem value="paused">Paused</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button onClick={() => setIsCreateDialogOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Journey
            </Button>
          </div>

          <div className="grid gap-6">
            {journeys.map((journey) => (
              <Card key={journey.id}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="font-semibold text-lg">{journey.name}</h3>
                        <Badge className={getStatusColor(journey.status)}>
                          {journey.status}
                        </Badge>
                      </div>
                      <p className="text-gray-600">{journey.description}</p>
                    </div>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <BarChart3 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-lg font-semibold">{journey.customerCount.toLocaleString()}</div>
                      <div className="text-sm text-gray-600">Customers</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-lg font-semibold">{journey.conversionRate}%</div>
                      <div className="text-sm text-gray-600">Conversion Rate</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-lg font-semibold">{journey.avgDuration}</div>
                      <div className="text-sm text-gray-600">Avg Duration</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-lg font-semibold">{journey.stages.length}</div>
                      <div className="text-sm text-gray-600">Stages</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-600">Journey Stages:</span>
                    <div className="flex gap-2 flex-wrap">
                      {journey.stages.map((stage, index) => (
                        <div key={index} className="flex items-center gap-1">
                          <Badge variant="outline">{stage}</Badge>
                          {index < journey.stages.length - 1 && (
                            <ArrowUpRight className="h-3 w-3 text-gray-400" />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Create Integration Dialog */}
      <CreateIntegrationDialog />
    </div>
  );
};

export { CDPPage };