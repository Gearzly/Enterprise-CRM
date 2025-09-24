import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Progress } from '../../components/ui/progress';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Plus, Target, TrendingUp, TrendingDown, Calendar, Users, DollarSign, Trophy } from 'lucide-react';
import { useState } from 'react';

export function TargetsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('current-quarter');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const targets = [
    {
      id: 1,
      title: 'Q1 Revenue Target',
      type: 'Revenue',
      period: 'Q1 2024',
      target: 500000,
      current: 387500,
      progress: 77.5,
      assignee: 'Sales Team',
      dueDate: '2024-03-31',
      status: 'On Track',
      description: 'Achieve $500K in total revenue for Q1'
    },
    {
      id: 2,
      title: 'New Customer Acquisition',
      type: 'Customers',
      period: 'January 2024',
      target: 50,
      current: 42,
      progress: 84,
      assignee: 'John Smith',
      dueDate: '2024-01-31',
      status: 'Ahead',
      description: 'Acquire 50 new customers this month'
    },
    {
      id: 3,
      title: 'Lead Conversion Rate',
      type: 'Conversion',
      period: 'Q1 2024',
      target: 25,
      current: 23.4,
      progress: 93.6,
      assignee: 'Marketing Team',
      dueDate: '2024-03-31',
      status: 'On Track',
      description: 'Maintain 25% lead conversion rate'
    },
    {
      id: 4,
      title: 'Product Demo Bookings',
      type: 'Activities',
      period: 'This Week',
      target: 20,
      current: 12,
      progress: 60,
      assignee: 'Sarah Johnson',
      dueDate: '2024-01-21',
      status: 'Behind',
      description: 'Schedule 20 product demos this week'
    },
    {
      id: 5,
      title: 'Upsell Revenue',
      type: 'Revenue',
      period: 'January 2024',
      target: 75000,
      current: 68200,
      progress: 90.9,
      assignee: 'Account Managers',
      dueDate: '2024-01-31',
      status: 'On Track',
      description: 'Generate $75K from existing customers'
    }
  ];

  const teamPerformance = [
    {
      name: 'John Smith',
      role: 'Senior Sales Rep',
      targetsAssigned: 8,
      targetsCompleted: 6,
      completionRate: 75,
      totalRevenue: '$125,000'
    },
    {
      name: 'Sarah Johnson',
      role: 'Sales Rep',
      targetsAssigned: 6,
      targetsCompleted: 5,
      completionRate: 83.3,
      totalRevenue: '$98,500'
    },
    {
      name: 'Mike Chen',
      role: 'Account Manager',
      targetsAssigned: 5,
      targetsCompleted: 4,
      completionRate: 80,
      totalRevenue: '$156,750'
    },
    {
      name: 'Emily Davis',
      role: 'Sales Rep',
      targetsAssigned: 7,
      targetsCompleted: 4,
      completionRate: 57.1,
      totalRevenue: '$87,200'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Ahead': return 'bg-green-500';
      case 'On Track': return 'bg-blue-500';
      case 'Behind': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'Ahead': return 'default';
      case 'On Track': return 'secondary';
      case 'Behind': return 'destructive';
      default: return 'outline';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Sales Targets</h1>
          <p className="text-muted-foreground">
            Set, track, and manage sales targets and goals
          </p>
        </div>
        <div className="flex gap-2">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-[180px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="current-quarter">Current Quarter</SelectItem>
              <SelectItem value="current-month">Current Month</SelectItem>
              <SelectItem value="current-week">Current Week</SelectItem>
              <SelectItem value="current-year">Current Year</SelectItem>
            </SelectContent>
          </Select>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                New Target
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Create New Target</DialogTitle>
                <DialogDescription>
                  Set a new sales target for your team or individual
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="title" className="text-right">
                    Title
                  </Label>
                  <Input id="title" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="type" className="text-right">
                    Type
                  </Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="revenue">Revenue</SelectItem>
                      <SelectItem value="customers">Customers</SelectItem>
                      <SelectItem value="conversion">Conversion</SelectItem>
                      <SelectItem value="activities">Activities</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="target" className="text-right">
                    Target
                  </Label>
                  <Input id="target" type="number" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="assignee" className="text-right">
                    Assignee
                  </Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select assignee" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="john">John Smith</SelectItem>
                      <SelectItem value="sarah">Sarah Johnson</SelectItem>
                      <SelectItem value="mike">Mike Chen</SelectItem>
                      <SelectItem value="emily">Emily Davis</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="description" className="text-right">
                    Description
                  </Label>
                  <Textarea id="description" className="col-span-3" />
                </div>
              </div>
              <DialogFooter>
                <Button type="submit" onClick={() => setIsCreateDialogOpen(false)}>
                  Create Target
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Target Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Targets</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+2</span> from last period
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completion Rate</CardTitle>
            <Trophy className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">78.5%</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+5.2%</span> from last period
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$487K</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+12.3%</span> vs target
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Team Members</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">
              Active contributors
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Active Targets */}
      <Card>
        <CardHeader>
          <CardTitle>Active Targets</CardTitle>
          <CardDescription>
            Track progress on current sales targets and goals
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {targets.map((target) => (
              <div key={target.id} className="border rounded-lg p-4">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-medium">{target.title}</h3>
                      <Badge variant={getStatusVariant(target.status)}>
                        {target.status}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">
                      {target.description}
                    </p>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span>Type: {target.type}</span>
                      <span>•</span>
                      <span>Period: {target.period}</span>
                      <span>•</span>
                      <span>Assignee: {target.assignee}</span>
                      <span>•</span>
                      <span>Due: {target.dueDate}</span>
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Edit
                  </Button>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Progress: {target.current} / {target.target}</span>
                    <span>{target.progress.toFixed(1)}%</span>
                  </div>
                  <Progress value={target.progress} className="h-2" />
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>
                      {target.type === 'Revenue' ? formatCurrency(target.current) : target.current} achieved
                    </span>
                    <span>
                      {target.type === 'Revenue' ? formatCurrency(target.target - target.current) : target.target - target.current} remaining
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Team Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Team Performance</CardTitle>
          <CardDescription>
            Individual performance against assigned targets
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {teamPerformance.map((member, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-medium">{member.name}</h3>
                    <Badge variant="outline">{member.role}</Badge>
                  </div>
                  <div className="flex items-center gap-6 text-sm text-muted-foreground">
                    <span>Targets: {member.targetsCompleted}/{member.targetsAssigned}</span>
                    <span>Revenue: {member.totalRevenue}</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-medium">{member.completionRate.toFixed(1)}%</div>
                  <div className="text-sm text-muted-foreground">Completion Rate</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}