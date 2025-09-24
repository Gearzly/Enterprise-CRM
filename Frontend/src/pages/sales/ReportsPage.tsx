import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Calendar, Download, Filter, TrendingUp, TrendingDown, DollarSign, Users, Target, BarChart3 } from 'lucide-react';
import { useState } from 'react';

export function ReportsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('this-month');
  const [selectedType, setSelectedType] = useState('all');

  const reports = [
    {
      id: 1,
      name: 'Monthly Sales Performance',
      type: 'Performance',
      period: 'Monthly',
      lastGenerated: '2024-01-15',
      status: 'Ready',
      revenue: '$125,000',
      growth: '+12.5%',
      isPositive: true
    },
    {
      id: 2,
      name: 'Lead Conversion Analysis',
      type: 'Conversion',
      period: 'Weekly',
      lastGenerated: '2024-01-14',
      status: 'Ready',
      revenue: '$89,500',
      growth: '+8.2%',
      isPositive: true
    },
    {
      id: 3,
      name: 'Team Performance Report',
      type: 'Team',
      period: 'Quarterly',
      lastGenerated: '2024-01-10',
      status: 'Generating',
      revenue: '$245,000',
      growth: '-2.1%',
      isPositive: false
    },
    {
      id: 4,
      name: 'Pipeline Analysis',
      type: 'Pipeline',
      period: 'Daily',
      lastGenerated: '2024-01-15',
      status: 'Ready',
      revenue: '$56,750',
      growth: '+15.3%',
      isPositive: true
    },
    {
      id: 5,
      name: 'Customer Acquisition Cost',
      type: 'Cost Analysis',
      period: 'Monthly',
      lastGenerated: '2024-01-12',
      status: 'Ready',
      revenue: '$1,250',
      growth: '-5.4%',
      isPositive: false
    }
  ];

  const quickStats = [
    {
      title: 'Total Revenue',
      value: '$487,250',
      change: '+18.2%',
      isPositive: true,
      icon: DollarSign
    },
    {
      title: 'Active Leads',
      value: '1,247',
      change: '+12.5%',
      isPositive: true,
      icon: Users
    },
    {
      title: 'Conversion Rate',
      value: '23.4%',
      change: '+2.1%',
      isPositive: true,
      icon: Target
    },
    {
      title: 'Reports Generated',
      value: '156',
      change: '+8.7%',
      isPositive: true,
      icon: BarChart3
    }
  ];

  const filteredReports = reports.filter(report => {
    if (selectedType === 'all') return true;
    return report.type.toLowerCase().includes(selectedType.toLowerCase());
  });

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Sales Reports</h1>
          <p className="text-muted-foreground">
            Generate comprehensive sales reports and analytics
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Calendar className="mr-2 h-4 w-4" />
            Schedule Report
          </Button>
          <Button>
            <Download className="mr-2 h-4 w-4" />
            Export All
          </Button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {quickStats.map((stat, index) => {
          const IconComponent = stat.icon;
          return (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <IconComponent className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                  {stat.isPositive ? (
                    <TrendingUp className="h-3 w-3 text-green-500" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500" />
                  )}
                  <span className={stat.isPositive ? 'text-green-500' : 'text-red-500'}>
                    {stat.change}
                  </span>
                  <span>from last period</span>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Report Filters</CardTitle>
          <CardDescription>Filter and customize your reports</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="text-sm font-medium">Time Period</label>
              <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="today">Today</SelectItem>
                  <SelectItem value="this-week">This Week</SelectItem>
                  <SelectItem value="this-month">This Month</SelectItem>
                  <SelectItem value="this-quarter">This Quarter</SelectItem>
                  <SelectItem value="this-year">This Year</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex-1">
              <label className="text-sm font-medium">Report Type</label>
              <Select value={selectedType} onValueChange={setSelectedType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="performance">Performance</SelectItem>
                  <SelectItem value="conversion">Conversion</SelectItem>
                  <SelectItem value="team">Team</SelectItem>
                  <SelectItem value="pipeline">Pipeline</SelectItem>
                  <SelectItem value="cost">Cost Analysis</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-end">
              <Button variant="outline">
                <Filter className="mr-2 h-4 w-4" />
                Apply Filters
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Reports List */}
      <Card>
        <CardHeader>
          <CardTitle>Available Reports</CardTitle>
          <CardDescription>
            View and download your sales reports
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredReports.map((report) => (
              <div
                key={report.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h3 className="font-medium">{report.name}</h3>
                    <Badge 
                      variant={report.status === 'Ready' ? 'default' : 'secondary'}
                    >
                      {report.status}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                    <span>Type: {report.type}</span>
                    <span>•</span>
                    <span>Period: {report.period}</span>
                    <span>•</span>
                    <span>Last Generated: {report.lastGenerated}</span>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <div className="font-medium">{report.revenue}</div>
                    <div className={`text-sm flex items-center gap-1 ${
                      report.isPositive ? 'text-green-500' : 'text-red-500'
                    }`}>
                      {report.isPositive ? (
                        <TrendingUp className="h-3 w-3" />
                      ) : (
                        <TrendingDown className="h-3 w-3" />
                      )}
                      {report.growth}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm"
                      disabled={report.status !== 'Ready'}
                    >
                      <Download className="h-4 w-4" />
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                    >
                      View
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}