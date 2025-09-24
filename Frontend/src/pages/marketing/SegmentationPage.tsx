import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Textarea } from '../../components/ui/textarea';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Label } from '../../components/ui/label';
import { Switch } from '../../components/ui/switch';
import { Progress } from '../../components/ui/progress';
import { Checkbox } from '../../components/ui/checkbox';
import { 
  Target, Plus, Filter, Search, Eye, Edit, Trash2, Users, 
  Calendar, Clock, User, Tag, Globe, FileText, BarChart3, 
  TrendingUp, Share2, Copy, Archive, Star, CheckCircle,
  AlertCircle, XCircle, PlayCircle, PauseCircle, RefreshCw,
  Zap, Settings, Download, Upload, PieChart, Activity,
  MapPin, DollarSign, ShoppingCart, Mail, Phone, Smartphone
} from 'lucide-react';

interface Segment {
  id: number;
  name: string;
  description: string;
  criteria: SegmentCriteria[];
  customerCount: number;
  status: 'active' | 'inactive' | 'draft';
  createdDate: string;
  lastUpdated: string;
  createdBy: string;
  tags: string[];
  conversionRate: number;
  avgOrderValue: number;
  lifetimeValue: number;
  engagementScore: number;
}

interface SegmentCriteria {
  field: string;
  operator: string;
  value: string | number;
  type: 'demographic' | 'behavioral' | 'geographic' | 'psychographic';
}

interface Campaign {
  id: number;
  name: string;
  segments: number[];
  status: 'active' | 'paused' | 'completed';
  reach: number;
  engagement: number;
  conversion: number;
  startDate: string;
  endDate?: string;
}

export function SegmentationPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedSegment, setSelectedSegment] = useState<Segment | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('segments');

  const segments: Segment[] = [
    {
      id: 1,
      name: 'High-Value Customers',
      description: 'Customers with high lifetime value and frequent purchases',
      criteria: [
        { field: 'totalSpent', operator: '>', value: 5000, type: 'behavioral' },
        { field: 'orderCount', operator: '>=', value: 10, type: 'behavioral' },
        { field: 'lastPurchase', operator: '<=', value: 30, type: 'behavioral' }
      ],
      customerCount: 2847,
      status: 'active',
      createdDate: '2024-01-15',
      lastUpdated: '2024-01-28',
      createdBy: 'Sarah Johnson',
      tags: ['high-value', 'loyal', 'premium'],
      conversionRate: 15.8,
      avgOrderValue: 450,
      lifetimeValue: 8500,
      engagementScore: 92
    },
    {
      id: 2,
      name: 'New Subscribers',
      description: 'Recently subscribed users who haven\'t made their first purchase',
      criteria: [
        { field: 'subscriptionDate', operator: '<=', value: 7, type: 'behavioral' },
        { field: 'orderCount', operator: '=', value: 0, type: 'behavioral' },
        { field: 'emailEngagement', operator: '>', value: 0.5, type: 'behavioral' }
      ],
      customerCount: 1523,
      status: 'active',
      createdDate: '2024-01-20',
      lastUpdated: '2024-01-30',
      createdBy: 'Mike Chen',
      tags: ['new', 'prospects', 'nurture'],
      conversionRate: 8.2,
      avgOrderValue: 0,
      lifetimeValue: 0,
      engagementScore: 65
    },
    {
      id: 3,
      name: 'Geographic - West Coast',
      description: 'Customers located in California, Oregon, and Washington',
      criteria: [
        { field: 'state', operator: 'in', value: 'CA,OR,WA', type: 'geographic' },
        { field: 'isActive', operator: '=', value: true, type: 'behavioral' }
      ],
      customerCount: 4521,
      status: 'active',
      createdDate: '2024-01-10',
      lastUpdated: '2024-01-25',
      createdBy: 'Emily Rodriguez',
      tags: ['geographic', 'west-coast', 'regional'],
      conversionRate: 12.4,
      avgOrderValue: 320,
      lifetimeValue: 2800,
      engagementScore: 78
    },
    {
      id: 4,
      name: 'Cart Abandoners',
      description: 'Users who added items to cart but didn\'t complete purchase',
      criteria: [
        { field: 'cartAbandonment', operator: '>', value: 0, type: 'behavioral' },
        { field: 'lastCartActivity', operator: '<=', value: 3, type: 'behavioral' },
        { field: 'emailOptIn', operator: '=', value: true, type: 'behavioral' }
      ],
      customerCount: 892,
      status: 'draft',
      createdDate: '2024-01-28',
      lastUpdated: '2024-01-30',
      createdBy: 'David Park',
      tags: ['cart-abandonment', 'retargeting', 'conversion'],
      conversionRate: 0,
      avgOrderValue: 0,
      lifetimeValue: 0,
      engagementScore: 45
    },
    {
      id: 5,
      name: 'Mobile Users',
      description: 'Customers who primarily engage through mobile devices',
      criteria: [
        { field: 'primaryDevice', operator: '=', value: 'mobile', type: 'behavioral' },
        { field: 'mobileAppInstalled', operator: '=', value: true, type: 'behavioral' },
        { field: 'lastActivity', operator: '<=', value: 7, type: 'behavioral' }
      ],
      customerCount: 6234,
      status: 'active',
      createdDate: '2024-01-12',
      lastUpdated: '2024-01-29',
      createdBy: 'Lisa Wang',
      tags: ['mobile', 'app-users', 'engagement'],
      conversionRate: 10.6,
      avgOrderValue: 180,
      lifetimeValue: 1200,
      engagementScore: 85
    }
  ];

  const campaigns: Campaign[] = [
    {
      id: 1,
      name: 'Premium Customer Retention',
      segments: [1],
      status: 'active',
      reach: 2847,
      engagement: 18.5,
      conversion: 12.3,
      startDate: '2024-01-15',
      endDate: '2024-02-15'
    },
    {
      id: 2,
      name: 'New Subscriber Welcome Series',
      segments: [2],
      status: 'active',
      reach: 1523,
      engagement: 24.7,
      conversion: 8.2,
      startDate: '2024-01-20'
    },
    {
      id: 3,
      name: 'West Coast Product Launch',
      segments: [3],
      status: 'paused',
      reach: 4521,
      engagement: 15.2,
      conversion: 9.8,
      startDate: '2024-01-10',
      endDate: '2024-01-31'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'inactive': return 'bg-red-100 text-red-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCampaignStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredSegments = segments.filter(segment => {
    const matchesSearch = segment.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         segment.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         segment.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = filterStatus === 'all' || segment.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const segmentStats = {
    total: segments.length,
    active: segments.filter(s => s.status === 'active').length,
    totalCustomers: segments.reduce((sum, s) => sum + s.customerCount, 0),
    avgConversion: segments.reduce((sum, s) => sum + s.conversionRate, 0) / segments.length
  };

  const CreateSegmentDialog = () => (
    <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Create New Segment</DialogTitle>
          <DialogDescription>
            Define criteria to create a customer segment for targeted marketing.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-6 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="segmentName">Segment Name</Label>
              <Input id="segmentName" placeholder="Enter segment name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="segmentTags">Tags (comma-separated)</Label>
              <Input id="segmentTags" placeholder="tag1, tag2, tag3" />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="segmentDescription">Description</Label>
            <Textarea id="segmentDescription" placeholder="Describe this segment" />
          </div>
          
          <div className="space-y-4">
            <Label className="text-base font-semibold">Segmentation Criteria</Label>
            
            <Tabs defaultValue="demographic" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="demographic">Demographic</TabsTrigger>
                <TabsTrigger value="behavioral">Behavioral</TabsTrigger>
                <TabsTrigger value="geographic">Geographic</TabsTrigger>
                <TabsTrigger value="psychographic">Psychographic</TabsTrigger>
              </TabsList>
              
              <TabsContent value="demographic" className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label>Age Range</Label>
                    <div className="flex gap-2">
                      <Input placeholder="Min" type="number" />
                      <Input placeholder="Max" type="number" />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Gender</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select gender" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All</SelectItem>
                        <SelectItem value="male">Male</SelectItem>
                        <SelectItem value="female">Female</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Income Range</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select range" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0-25k">$0 - $25,000</SelectItem>
                        <SelectItem value="25k-50k">$25,000 - $50,000</SelectItem>
                        <SelectItem value="50k-75k">$50,000 - $75,000</SelectItem>
                        <SelectItem value="75k-100k">$75,000 - $100,000</SelectItem>
                        <SelectItem value="100k+">$100,000+</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="behavioral" className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Purchase Frequency</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select frequency" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="first-time">First-time buyers</SelectItem>
                        <SelectItem value="occasional">Occasional (1-3 purchases)</SelectItem>
                        <SelectItem value="regular">Regular (4-10 purchases)</SelectItem>
                        <SelectItem value="frequent">Frequent (10+ purchases)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Total Spent</Label>
                    <div className="flex gap-2">
                      <Input placeholder="Min amount" type="number" />
                      <Input placeholder="Max amount" type="number" />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Last Purchase</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select timeframe" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="7">Last 7 days</SelectItem>
                        <SelectItem value="30">Last 30 days</SelectItem>
                        <SelectItem value="90">Last 90 days</SelectItem>
                        <SelectItem value="365">Last year</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Email Engagement</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select engagement" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="high">High (&gt;50% open rate)</SelectItem>
                        <SelectItem value="medium">Medium (20-50% open rate)</SelectItem>
                        <SelectItem value="low">Low (&lt;20% open rate)</SelectItem>
                        <SelectItem value="none">No engagement</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="geographic" className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Country</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select country" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="us">United States</SelectItem>
                        <SelectItem value="ca">Canada</SelectItem>
                        <SelectItem value="uk">United Kingdom</SelectItem>
                        <SelectItem value="au">Australia</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>State/Province</Label>
                    <Input placeholder="Enter state or province" />
                  </div>
                  <div className="space-y-2">
                    <Label>City</Label>
                    <Input placeholder="Enter city" />
                  </div>
                  <div className="space-y-2">
                    <Label>Timezone</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select timezone" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pst">Pacific (PST)</SelectItem>
                        <SelectItem value="mst">Mountain (MST)</SelectItem>
                        <SelectItem value="cst">Central (CST)</SelectItem>
                        <SelectItem value="est">Eastern (EST)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="psychographic" className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Interests</Label>
                    <div className="space-y-2">
                      {['Technology', 'Fashion', 'Sports', 'Travel', 'Food', 'Health'].map((interest) => (
                        <div key={interest} className="flex items-center space-x-2">
                          <Checkbox id={interest} />
                          <Label htmlFor={interest}>{interest}</Label>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Lifestyle</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select lifestyle" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="budget-conscious">Budget Conscious</SelectItem>
                        <SelectItem value="premium">Premium Seekers</SelectItem>
                        <SelectItem value="convenience">Convenience Focused</SelectItem>
                        <SelectItem value="eco-friendly">Eco-Friendly</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(false)}>
            Create Segment
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <Target className="h-8 w-8 text-blue-600" />
            Segmentation & Targeting
          </h1>
          <p className="text-muted-foreground">
            Create and manage customer segments for targeted marketing campaigns
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Create Segment
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Segments</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{segmentStats.total}</div>
            <p className="text-xs text-muted-foreground">
              {segmentStats.active} active
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Customers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{segmentStats.totalCustomers.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Across all segments
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Conversion</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{segmentStats.avgConversion.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Segment average
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Campaigns</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{campaigns.filter(c => c.status === 'active').length}</div>
            <p className="text-xs text-muted-foreground">
              Running campaigns
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="segments">Segments</TabsTrigger>
          <TabsTrigger value="campaigns">Targeted Campaigns</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="segments" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Customer Segments</CardTitle>
              <CardDescription>
                Manage your customer segments and targeting criteria
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4 mb-6">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="Search segments..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="inactive">Inactive</SelectItem>
                    <SelectItem value="draft">Draft</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Segment</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Customers</TableHead>
                      <TableHead>Conversion Rate</TableHead>
                      <TableHead>Avg. Order Value</TableHead>
                      <TableHead>Engagement</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredSegments.map((segment) => (
                      <TableRow key={segment.id}>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="font-medium">{segment.name}</div>
                            <p className="text-sm text-muted-foreground">{segment.description}</p>
                            <div className="flex items-center gap-1">
                              {segment.tags.map((tag, index) => (
                                <Badge key={index} variant="secondary" className="text-xs">
                                  {tag}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge className={getStatusColor(segment.status)}>
                            {segment.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Users className="h-4 w-4 text-muted-foreground" />
                            {segment.customerCount.toLocaleString()}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <TrendingUp className="h-4 w-4 text-muted-foreground" />
                            {segment.conversionRate}%
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <DollarSign className="h-4 w-4 text-muted-foreground" />
                            ${segment.avgOrderValue}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Progress value={segment.engagementScore} className="w-16" />
                            <span className="text-sm">{segment.engagementScore}%</span>
                          </div>
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex items-center justify-end gap-2">
                            <Button variant="ghost" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Copy className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm" className="text-red-600">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="campaigns" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Targeted Campaigns</CardTitle>
              <CardDescription>
                View campaigns targeting specific customer segments
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Campaign</TableHead>
                      <TableHead>Segments</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Reach</TableHead>
                      <TableHead>Engagement</TableHead>
                      <TableHead>Conversion</TableHead>
                      <TableHead>Duration</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {campaigns.map((campaign) => (
                      <TableRow key={campaign.id}>
                        <TableCell className="font-medium">{campaign.name}</TableCell>
                        <TableCell>
                          <div className="flex gap-1">
                            {campaign.segments.map((segmentId) => {
                              const segment = segments.find(s => s.id === segmentId);
                              return segment ? (
                                <Badge key={segmentId} variant="outline" className="text-xs">
                                  {segment.name}
                                </Badge>
                              ) : null;
                            })}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge className={getCampaignStatusColor(campaign.status)}>
                            {campaign.status}
                          </Badge>
                        </TableCell>
                        <TableCell>{campaign.reach.toLocaleString()}</TableCell>
                        <TableCell>{campaign.engagement}%</TableCell>
                        <TableCell>{campaign.conversion}%</TableCell>
                        <TableCell>
                          <div className="text-sm">
                            {campaign.startDate}
                            {campaign.endDate && ` - ${campaign.endDate}`}
                          </div>
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex items-center justify-end gap-2">
                            <Button variant="ghost" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            {campaign.status === 'active' ? (
                              <Button variant="ghost" size="sm">
                                <PauseCircle className="h-4 w-4" />
                              </Button>
                            ) : (
                              <Button variant="ghost" size="sm">
                                <PlayCircle className="h-4 w-4" />
                              </Button>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Segment Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {segments.slice(0, 3).map((segment) => (
                    <div key={segment.id} className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">{segment.name}</div>
                        <div className="text-sm text-muted-foreground">
                          {segment.customerCount.toLocaleString()} customers
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">{segment.conversionRate}%</div>
                        <div className="text-sm text-muted-foreground">conversion</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Segment Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {segments.map((segment) => (
                    <div key={segment.id} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>{segment.name}</span>
                        <span>{((segment.customerCount / segmentStats.totalCustomers) * 100).toFixed(1)}%</span>
                      </div>
                      <Progress 
                        value={(segment.customerCount / segmentStats.totalCustomers) * 100} 
                        className="h-2"
                      />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      <CreateSegmentDialog />
    </div>
  );
}