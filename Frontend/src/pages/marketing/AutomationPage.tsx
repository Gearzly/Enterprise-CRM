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
import { Switch } from '../../components/ui/switch';
import { Plus, Play, Pause, Edit, Zap, Users, Mail, Clock, TrendingUp, ArrowRight, Bot, Workflow } from 'lucide-react';
import { useState } from 'react';

export function AutomationPage() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [selectedStatus, setSelectedStatus] = useState('all');

  const workflows = [
    {
      id: 1,
      name: 'Welcome Email Series',
      description: 'Automated welcome sequence for new subscribers',
      trigger: 'User signup',
      status: 'Active',
      totalRuns: 1250,
      successRate: 94.5,
      lastRun: '2024-01-15 14:30',
      steps: 5,
      category: 'Onboarding'
    },
    {
      id: 2,
      name: 'Abandoned Cart Recovery',
      description: 'Re-engage users who abandoned their cart',
      trigger: 'Cart abandonment',
      status: 'Active',
      totalRuns: 890,
      successRate: 67.2,
      lastRun: '2024-01-15 16:45',
      steps: 3,
      category: 'E-commerce'
    },
    {
      id: 3,
      name: 'Lead Scoring Update',
      description: 'Automatically update lead scores based on activity',
      trigger: 'User activity',
      status: 'Active',
      totalRuns: 3450,
      successRate: 99.1,
      lastRun: '2024-01-15 17:00',
      steps: 2,
      category: 'Lead Management'
    },
    {
      id: 4,
      name: 'Trial Expiration Reminder',
      description: 'Notify users before their trial expires',
      trigger: 'Trial period',
      status: 'Paused',
      totalRuns: 245,
      successRate: 78.6,
      lastRun: '2024-01-12 09:00',
      steps: 4,
      category: 'Retention'
    },
    {
      id: 5,
      name: 'Customer Satisfaction Survey',
      description: 'Send survey after support ticket closure',
      trigger: 'Ticket closed',
      status: 'Draft',
      totalRuns: 0,
      successRate: 0,
      lastRun: null,
      steps: 3,
      category: 'Feedback'
    }
  ];

  const templates = [
    {
      id: 1,
      name: 'Email Drip Campaign',
      description: 'Send a series of emails over time',
      category: 'Email Marketing',
      popularity: 95
    },
    {
      id: 2,
      name: 'Lead Nurturing Sequence',
      description: 'Nurture leads through the sales funnel',
      category: 'Lead Management',
      popularity: 87
    },
    {
      id: 3,
      name: 'Customer Onboarding',
      description: 'Guide new customers through setup',
      category: 'Onboarding',
      popularity: 92
    },
    {
      id: 4,
      name: 'Re-engagement Campaign',
      description: 'Win back inactive customers',
      category: 'Retention',
      popularity: 78
    }
  ];

  const triggers = [
    { name: 'User Signup', count: 1250, icon: Users },
    { name: 'Email Opened', count: 3400, icon: Mail },
    { name: 'Page Visit', count: 5600, icon: TrendingUp },
    { name: 'Cart Abandonment', count: 890, icon: Clock },
    { name: 'Trial Started', count: 245, icon: Play },
    { name: 'Subscription Cancelled', count: 67, icon: Pause }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'default';
      case 'Paused': return 'secondary';
      case 'Draft': return 'outline';
      default: return 'outline';
    }
  };

  const filteredWorkflows = workflows.filter(workflow => {
    if (selectedStatus === 'all') return true;
    return workflow.status === selectedStatus;
  });

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Marketing Automation</h1>
          <p className="text-muted-foreground">
            Automate marketing workflows and processes
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Workflow className="mr-2 h-4 w-4" />
            Workflow Builder
          </Button>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                New Automation
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Create New Automation</DialogTitle>
                <DialogDescription>
                  Set up a new marketing automation workflow
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">Name</Label>
                  <Input id="name" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="template" className="text-right">Template</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Choose a template" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="email-drip">Email Drip Campaign</SelectItem>
                      <SelectItem value="lead-nurturing">Lead Nurturing</SelectItem>
                      <SelectItem value="onboarding">Customer Onboarding</SelectItem>
                      <SelectItem value="re-engagement">Re-engagement</SelectItem>
                      <SelectItem value="custom">Start from Scratch</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="trigger" className="text-right">Trigger</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select trigger event" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="signup">User Signup</SelectItem>
                      <SelectItem value="email-open">Email Opened</SelectItem>
                      <SelectItem value="page-visit">Page Visit</SelectItem>
                      <SelectItem value="cart-abandon">Cart Abandonment</SelectItem>
                      <SelectItem value="trial-start">Trial Started</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="description" className="text-right">Description</Label>
                  <Textarea id="description" className="col-span-3" />
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Save as Draft
                </Button>
                <Button onClick={() => setIsCreateDialogOpen(false)}>
                  Create & Configure
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Automation Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Workflows</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {workflows.filter(w => w.status === 'Active').length}
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+2</span> this month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Executions</CardTitle>
            <Play className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {workflows.reduce((sum, w) => sum + w.totalRuns, 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+18%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(workflows.reduce((sum, w) => sum + w.successRate, 0) / workflows.length)}%
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+3%</span> improvement
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Time Saved</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">124h</div>
            <p className="text-xs text-muted-foreground">
              This month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="workflows" className="space-y-4">
        <TabsList>
          <TabsTrigger value="workflows">Workflows</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="triggers">Triggers</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="workflows" className="space-y-4">
          {/* Workflow Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex gap-4">
                <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="Active">Active</SelectItem>
                    <SelectItem value="Paused">Paused</SelectItem>
                    <SelectItem value="Draft">Draft</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Workflows Table */}
          <Card>
            <CardHeader>
              <CardTitle>Marketing Automation Workflows</CardTitle>
              <CardDescription>
                {filteredWorkflows.length} workflows found
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Workflow</TableHead>
                    <TableHead>Trigger</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Performance</TableHead>
                    <TableHead>Last Run</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredWorkflows.map((workflow) => (
                    <TableRow key={workflow.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{workflow.name}</div>
                          <div className="text-sm text-muted-foreground">{workflow.description}</div>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant="outline" className="text-xs">
                              {workflow.category}
                            </Badge>
                            <span className="text-xs text-muted-foreground">
                              {workflow.steps} steps
                            </span>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Zap className="h-4 w-4 text-muted-foreground" />
                          {workflow.trigger}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Badge variant={getStatusColor(workflow.status)}>
                            {workflow.status}
                          </Badge>
                          {workflow.status === 'Active' && (
                            <Switch size="sm" checked={true} />
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div>
                          <div className="font-medium">{workflow.totalRuns} runs</div>
                          <div className="text-sm text-muted-foreground">
                            {workflow.successRate}% success rate
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        {workflow.lastRun || <span className="text-muted-foreground">Never</span>}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="outline" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          {workflow.status === 'Active' ? (
                            <Button variant="outline" size="sm">
                              <Pause className="h-4 w-4" />
                            </Button>
                          ) : (
                            <Button variant="outline" size="sm">
                              <Play className="h-4 w-4" />
                            </Button>
                          )}
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
              <CardTitle>Automation Templates</CardTitle>
              <CardDescription>
                Pre-built templates to get you started quickly
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {templates.map((template) => (
                  <Card key={template.id} className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-base">{template.name}</CardTitle>
                        <Badge variant="secondary">{template.popularity}% popular</Badge>
                      </div>
                      <CardDescription>{template.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between">
                        <Badge variant="outline">{template.category}</Badge>
                        <Button size="sm">
                          Use Template
                          <ArrowRight className="ml-2 h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="triggers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Automation Triggers</CardTitle>
              <CardDescription>
                Events that can trigger your automation workflows
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {triggers.map((trigger, index) => {
                  const IconComponent = trigger.icon;
                  return (
                    <Card key={index} className="hover:shadow-md transition-shadow">
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <IconComponent className="h-6 w-6 text-primary" />
                            <CardTitle className="text-base">{trigger.name}</CardTitle>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="text-2xl font-bold">{trigger.count.toLocaleString()}</div>
                            <div className="text-sm text-muted-foreground">triggers this month</div>
                          </div>
                          <Button variant="outline" size="sm">
                            Configure
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Automation Analytics</CardTitle>
              <CardDescription>
                Performance insights for your automation workflows
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Bot className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                <h3 className="font-medium mb-2">Detailed Analytics Coming Soon</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Get insights into workflow performance, conversion rates, and optimization opportunities
                </p>
                <Button variant="outline">
                  Request Early Access
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}