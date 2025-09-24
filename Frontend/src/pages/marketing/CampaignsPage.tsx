import { useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Progress } from '../../components/ui/progress';
import { Megaphone, Plus, Filter, Search, Eye, MousePointer, Users, DollarSign, Calendar, Mail, Play, Pause } from 'lucide-react';

export function CampaignsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const campaigns = [
    {
      id: 1,
      name: 'Spring Product Launch',
      type: 'Email + Social',
      status: 'active',
      startDate: '2024-01-01',
      endDate: '2024-03-31',
      budget: '$25,000',
      spent: '$18,500',
      impressions: 125000,
      clicks: 3420,
      conversions: 156,
      ctr: 2.74,
      conversionRate: 4.56,
      roi: '340%'
    },
    {
      id: 2,
      name: 'Customer Retention Campaign',
      type: 'Email',
      status: 'active',
      startDate: '2024-01-15',
      endDate: '2024-02-15',
      budget: '$15,000',
      spent: '$12,300',
      impressions: 85000,
      clicks: 2150,
      conversions: 89,
      ctr: 2.53,
      conversionRate: 4.14,
      roi: '285%'
    },
    {
      id: 3,
      name: 'Holiday Promotion',
      type: 'Multi-channel',
      status: 'completed',
      startDate: '2023-11-01',
      endDate: '2023-12-31',
      budget: '$50,000',
      spent: '$48,750',
      impressions: 320000,
      clicks: 8960,
      conversions: 524,
      ctr: 2.8,
      conversionRate: 5.85,
      roi: '450%'
    },
    {
      id: 4,
      name: 'New Feature Announcement',
      type: 'Social Media',
      status: 'draft',
      startDate: '2024-02-01',
      endDate: '2024-02-28',
      budget: '$20,000',
      spent: '$0',
      impressions: 0,
      clicks: 0,
      conversions: 0,
      ctr: 0,
      conversionRate: 0,
      roi: '0%'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      case 'paused': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = campaign.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         campaign.type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || campaign.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const totalBudget = campaigns.reduce((sum, campaign) => sum + parseInt(campaign.budget.replace(/[$,]/g, '')), 0);
  const totalSpent = campaigns.reduce((sum, campaign) => sum + parseInt(campaign.spent.replace(/[$,]/g, '')), 0);
  const totalImpressions = campaigns.reduce((sum, campaign) => sum + campaign.impressions, 0);
  const totalConversions = campaigns.reduce((sum, campaign) => sum + campaign.conversions, 0);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Marketing Campaigns</h1>
          <p className="text-muted-foreground">Plan, execute, and track marketing campaigns across channels</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Templates</Button>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            New Campaign
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Megaphone className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Active Campaigns</p>
              <p className="text-xl font-semibold">{campaigns.filter(c => c.status === 'active').length}</p>
              <p className="text-xs text-green-600">2 launching soon</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <DollarSign className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Budget</p>
              <p className="text-xl font-semibold">${(totalBudget / 1000).toFixed(0)}K</p>
              <p className="text-xs text-muted-foreground">${(totalSpent / 1000).toFixed(0)}K spent</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Eye className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Impressions</p>
              <p className="text-xl font-semibold">{(totalImpressions / 1000).toFixed(0)}K</p>
              <p className="text-xs text-green-600">+15% this month</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <MousePointer className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Conversions</p>
              <p className="text-xl font-semibold">{totalConversions}</p>
              <p className="text-xs text-green-600">4.2% avg rate</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Campaign Performance Overview */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Campaign Performance Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm">Budget Utilization</span>
              <span className="text-sm font-medium">{((totalSpent / totalBudget) * 100).toFixed(1)}%</span>
            </div>
            <Progress value={(totalSpent / totalBudget) * 100} className="h-2" />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm">Avg. Click-through Rate</span>
              <span className="text-sm font-medium">2.69%</span>
            </div>
            <Progress value={85} className="h-2" />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm">Avg. Conversion Rate</span>
              <span className="text-sm font-medium">4.89%</span>
            </div>
            <Progress value={75} className="h-2" />
          </div>
        </div>
      </Card>

      {/* Filters and Search */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search campaigns..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={filterStatus} onValueChange={setFilterStatus}>
          <SelectTrigger className="w-[200px]">
            <Filter className="w-4 h-4 mr-2" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
            <SelectItem value="draft">Draft</SelectItem>
            <SelectItem value="paused">Paused</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Campaigns Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Campaign</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Duration</TableHead>
              <TableHead>Budget</TableHead>
              <TableHead>Performance</TableHead>
              <TableHead>ROI</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredCampaigns.map((campaign) => (
              <TableRow key={campaign.id}>
                <TableCell>
                  <div>
                    <div className="font-medium">{campaign.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {campaign.impressions.toLocaleString()} impressions
                    </div>
                  </div>
                </TableCell>
                <TableCell>{campaign.type}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Badge className={getStatusColor(campaign.status)}>
                      {campaign.status}
                    </Badge>
                    {campaign.status === 'active' && (
                      <Button variant="ghost" size="sm">
                        <Pause className="w-3 h-3" />
                      </Button>
                    )}
                    {campaign.status === 'draft' && (
                      <Button variant="ghost" size="sm">
                        <Play className="w-3 h-3" />
                      </Button>
                    )}
                  </div>
                </TableCell>
                <TableCell>
                  <div className="text-sm">
                    <div>{campaign.startDate}</div>
                    <div className="text-muted-foreground">to {campaign.endDate}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <div>
                    <div className="font-medium">{campaign.budget}</div>
                    <div className="text-sm text-muted-foreground">
                      {campaign.spent} spent
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="text-sm">
                    <div>{campaign.clicks.toLocaleString()} clicks</div>
                    <div>{campaign.conversions} conversions</div>
                    <div className="text-muted-foreground">CTR: {campaign.ctr}%</div>
                  </div>
                </TableCell>
                <TableCell>
                  <span className={`font-medium ${campaign.roi !== '0%' ? 'text-green-600' : 'text-gray-500'}`}>
                    {campaign.roi}
                  </span>
                </TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Edit</Button>
                    <Button variant="outline" size="sm">Analytics</Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
}