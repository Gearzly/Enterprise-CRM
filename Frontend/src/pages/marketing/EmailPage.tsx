import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Progress } from '../../components/ui/progress';
import { Plus, Mail, Send, Users, Eye, MousePointer, BarChart3, Calendar, Play, Pause, Edit } from 'lucide-react';
import { useState } from 'react';

export function EmailPage() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [selectedStatus, setSelectedStatus] = useState('all');

  const campaigns = [
    {
      id: 1,
      name: 'Product Launch Announcement',
      subject: 'Introducing Our Revolutionary New Feature',
      status: 'Sent',
      sentDate: '2024-01-15',
      recipients: 5420,
      opened: 2167,
      clicked: 354,
      bounced: 28,
      unsubscribed: 12,
      openRate: 40.0,
      clickRate: 6.5,
      template: 'Product Launch'
    },
    {
      id: 2,
      name: 'Weekly Newsletter #47',
      subject: 'This Week in Industry Insights',
      status: 'Scheduled',
      sentDate: '2024-01-18',
      recipients: 8950,
      opened: 0,
      clicked: 0,
      bounced: 0,
      unsubscribed: 0,
      openRate: 0,
      clickRate: 0,
      template: 'Newsletter'
    },
    {
      id: 3,
      name: 'Webinar Invitation',
      subject: 'Join Our Exclusive Webinar Next Week',
      status: 'Draft',
      sentDate: null,
      recipients: 0,
      opened: 0,
      clicked: 0,
      bounced: 0,
      unsubscribed: 0,
      openRate: 0,
      clickRate: 0,
      template: 'Event Invitation'
    },
    {
      id: 4,
      name: 'Customer Success Stories',
      subject: 'See How Companies Like Yours Succeed',
      status: 'Sent',
      sentDate: '2024-01-12',
      recipients: 3200,
      opened: 1248,
      clicked: 187,
      bounced: 15,
      unsubscribed: 8,
      openRate: 39.0,
      clickRate: 5.8,
      template: 'Case Study'
    },
    {
      id: 5,
      name: 'Free Trial Reminder',
      subject: 'Your Trial Expires Soon - Upgrade Today',
      status: 'Sending',
      sentDate: '2024-01-16',
      recipients: 1250,
      opened: 342,
      clicked: 89,
      bounced: 7,
      unsubscribed: 3,
      openRate: 27.4,
      clickRate: 7.1,
      template: 'Trial Reminder'
    }
  ];

  const templates = [
    {
      id: 1,
      name: 'Welcome Series - Email 1',
      category: 'Onboarding',
      lastUsed: '2024-01-10',
      timesUsed: 45
    },
    {
      id: 2,
      name: 'Product Launch Announcement',
      category: 'Product Updates',
      lastUsed: '2024-01-15',
      timesUsed: 12
    },
    {
      id: 3,
      name: 'Weekly Newsletter Template',
      category: 'Newsletter',
      lastUsed: '2024-01-08',
      timesUsed: 47
    },
    {
      id: 4,
      name: 'Event Invitation',
      category: 'Events',
      lastUsed: '2024-01-05',
      timesUsed: 23
    },
    {
      id: 5,
      name: 'Customer Survey',
      category: 'Feedback',
      lastUsed: '2024-01-03',
      timesUsed: 18
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Sent': return 'default';
      case 'Scheduled': return 'secondary';
      case 'Draft': return 'outline';
      case 'Sending': return 'secondary';
      default: return 'outline';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Sent': return <Mail className="h-3 w-3" />;
      case 'Scheduled': return <Calendar className="h-3 w-3" />;
      case 'Draft': return <Edit className="h-3 w-3" />;
      case 'Sending': return <Send className="h-3 w-3" />;
      default: return <Mail className="h-3 w-3" />;
    }
  };

  const filteredCampaigns = campaigns.filter(campaign => {
    if (selectedStatus === 'all') return true;
    return campaign.status === selectedStatus;
  });

  const totalStats = {
    totalSent: campaigns.reduce((sum, c) => sum + c.recipients, 0),
    totalOpened: campaigns.reduce((sum, c) => sum + c.opened, 0),
    totalClicked: campaigns.reduce((sum, c) => sum + c.clicked, 0),
    avgOpenRate: campaigns.filter(c => c.recipients > 0).reduce((sum, c) => sum + c.openRate, 0) / campaigns.filter(c => c.recipients > 0).length || 0,
    avgClickRate: campaigns.filter(c => c.recipients > 0).reduce((sum, c) => sum + c.clickRate, 0) / campaigns.filter(c => c.recipients > 0).length || 0
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Email Marketing</h1>
          <p className="text-muted-foreground">
            Create and manage email marketing campaigns
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <BarChart3 className="mr-2 h-4 w-4" />
            Analytics
          </Button>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                New Campaign
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Create Email Campaign</DialogTitle>
                <DialogDescription>
                  Create a new email marketing campaign
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="campaign-name" className="text-right">Name</Label>
                  <Input id="campaign-name" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="subject" className="text-right">Subject</Label>
                  <Input id="subject" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="template" className="text-right">Template</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select template" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="newsletter">Newsletter</SelectItem>
                      <SelectItem value="product-launch">Product Launch</SelectItem>
                      <SelectItem value="event">Event Invitation</SelectItem>
                      <SelectItem value="welcome">Welcome Series</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="audience" className="text-right">Audience</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select audience" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all-subscribers">All Subscribers</SelectItem>
                      <SelectItem value="active-users">Active Users</SelectItem>
                      <SelectItem value="trial-users">Trial Users</SelectItem>
                      <SelectItem value="customers">Customers</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Save as Draft
                </Button>
                <Button onClick={() => setIsCreateDialogOpen(false)}>
                  Create Campaign
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Email Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Sent</CardTitle>
            <Send className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.totalSent.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+12%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Emails Opened</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.totalOpened.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+8%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Clicks</CardTitle>
            <MousePointer className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.totalClicked.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+15%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Open Rate</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.avgOpenRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Industry avg: 22%
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Click Rate</CardTitle>
            <MousePointer className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.avgClickRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Industry avg: 3.5%
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="campaigns" className="space-y-4">
        <TabsList>
          <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="audiences">Audiences</TabsTrigger>
        </TabsList>

        <TabsContent value="campaigns" className="space-y-4">
          {/* Campaign Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex gap-4">
                <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="Draft">Draft</SelectItem>
                    <SelectItem value="Scheduled">Scheduled</SelectItem>
                    <SelectItem value="Sending">Sending</SelectItem>
                    <SelectItem value="Sent">Sent</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Campaigns Table */}
          <Card>
            <CardHeader>
              <CardTitle>Email Campaigns</CardTitle>
              <CardDescription>
                {filteredCampaigns.length} campaigns found
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Campaign</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Recipients</TableHead>
                    <TableHead>Open Rate</TableHead>
                    <TableHead>Click Rate</TableHead>
                    <TableHead>Sent Date</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredCampaigns.map((campaign) => (
                    <TableRow key={campaign.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{campaign.name}</div>
                          <div className="text-sm text-muted-foreground">{campaign.subject}</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusColor(campaign.status)} className="gap-1">
                          {getStatusIcon(campaign.status)}
                          {campaign.status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div>
                          <div className="font-medium">{campaign.recipients.toLocaleString()}</div>
                          {campaign.status === 'Sent' && (
                            <div className="text-sm text-muted-foreground">
                              {campaign.opened} opened, {campaign.clicked} clicked
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        {campaign.status === 'Sent' ? (
                          <div>
                            <div className="font-medium">{campaign.openRate.toFixed(1)}%</div>
                            <Progress value={campaign.openRate} className="h-1 w-16" />
                          </div>
                        ) : (
                          <span className="text-muted-foreground">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {campaign.status === 'Sent' ? (
                          <div>
                            <div className="font-medium">{campaign.clickRate.toFixed(1)}%</div>
                            <Progress value={campaign.clickRate * 4} className="h-1 w-16" />
                          </div>
                        ) : (
                          <span className="text-muted-foreground">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {campaign.sentDate || <span className="text-muted-foreground">Not sent</span>}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          {campaign.status === 'Draft' && (
                            <Button variant="outline" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                          )}
                          {campaign.status === 'Scheduled' && (
                            <Button variant="outline" size="sm">
                              <Pause className="h-4 w-4" />
                            </Button>
                          )}
                          <Button variant="outline" size="sm">
                            View
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="templates" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Email Templates</CardTitle>
              <CardDescription>
                Manage reusable email templates
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {templates.map((template) => (
                  <Card key={template.id} className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardHeader>
                      <CardTitle className="text-base">{template.name}</CardTitle>
                      <CardDescription>{template.category}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2 text-sm text-muted-foreground">
                        <div>Last used: {template.lastUsed}</div>
                        <div>Used {template.timesUsed} times</div>
                      </div>
                      <div className="flex gap-2 mt-4">
                        <Button variant="outline" size="sm" className="flex-1">
                          Edit
                        </Button>
                        <Button size="sm" className="flex-1">
                          Use Template
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="audiences" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Email Audiences</CardTitle>
              <CardDescription>
                Manage your email subscriber segments
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium">All Subscribers</h3>
                    <p className="text-sm text-muted-foreground">Everyone on your email list</p>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">12,450</div>
                    <div className="text-sm text-muted-foreground">subscribers</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium">Active Users</h3>
                    <p className="text-sm text-muted-foreground">Users who logged in within 30 days</p>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">8,920</div>
                    <div className="text-sm text-muted-foreground">subscribers</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium">Trial Users</h3>
                    <p className="text-sm text-muted-foreground">Users currently on trial</p>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">1,250</div>
                    <div className="text-sm text-muted-foreground">subscribers</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium">Paying Customers</h3>
                    <p className="text-sm text-muted-foreground">Active paying subscribers</p>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">3,180</div>
                    <div className="text-sm text-muted-foreground">subscribers</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}