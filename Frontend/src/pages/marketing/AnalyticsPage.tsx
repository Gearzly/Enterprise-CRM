import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Progress } from '../../components/ui/progress';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, Users, Eye, MousePointer, DollarSign, Globe, Smartphone, Monitor, Calendar } from 'lucide-react';
import { useState } from 'react';

export function AnalyticsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('last-30-days');
  const [selectedMetric, setSelectedMetric] = useState('all');

  const performanceData = [
    { name: 'Jan', visitors: 4200, leads: 180, conversions: 45, revenue: 22500 },
    { name: 'Feb', visitors: 5100, leads: 220, conversions: 58, revenue: 29000 },
    { name: 'Mar', visitors: 4800, leads: 195, conversions: 52, revenue: 26000 },
    { name: 'Apr', visitors: 6200, leads: 275, conversions: 71, revenue: 35500 },
    { name: 'May', visitors: 5800, leads: 240, conversions: 63, revenue: 31500 },
    { name: 'Jun', visitors: 7100, leads: 310, conversions: 82, revenue: 41000 },
  ];

  const channelData = [
    { name: 'Organic Search', value: 35, visitors: 2485, color: '#8884d8' },
    { name: 'Social Media', value: 25, visitors: 1775, color: '#82ca9d' },
    { name: 'Email Marketing', value: 20, visitors: 1420, color: '#ffc658' },
    { name: 'Direct Traffic', value: 12, visitors: 852, color: '#ff7300' },
    { name: 'Paid Ads', value: 8, visitors: 568, color: '#00ff88' },
  ];

  const conversionFunnelData = [
    { stage: 'Visitors', count: 7100, percentage: 100 },
    { stage: 'Leads', count: 1420, percentage: 20 },
    { stage: 'Qualified', count: 568, percentage: 8 },
    { stage: 'Opportunities', count: 213, percentage: 3 },
    { stage: 'Customers', count: 82, percentage: 1.2 },
  ];

  const deviceData = [
    { device: 'Desktop', sessions: 4260, percentage: 60 },
    { device: 'Mobile', sessions: 2130, percentage: 30 },
    { device: 'Tablet', sessions: 710, percentage: 10 },
  ];

  const topPages = [
    { page: '/landing/product-demo', views: 1250, conversions: 45, conversionRate: 3.6 },
    { page: '/blog/industry-trends-2024', views: 890, conversions: 12, conversionRate: 1.3 },
    { page: '/pricing', views: 780, conversions: 32, conversionRate: 4.1 },
    { page: '/features/analytics', views: 650, conversions: 18, conversionRate: 2.8 },
    { page: '/case-studies', views: 520, conversions: 8, conversionRate: 1.5 },
  ];

  const campaignPerformance = [
    { campaign: 'Q2 Product Launch', impressions: 125000, clicks: 3750, ctr: 3.0, conversions: 158, cost: 2800 },
    { campaign: 'Brand Awareness', impressions: 89000, clicks: 2140, ctr: 2.4, conversions: 89, cost: 1950 },
    { campaign: 'Retargeting Campaign', impressions: 45000, clicks: 1350, ctr: 3.0, conversions: 67, cost: 1200 },
    { campaign: 'Lead Generation', impressions: 67000, clicks: 2010, ctr: 3.0, conversions: 134, cost: 2100 },
  ];

  const keyMetrics = [
    {
      title: 'Total Visitors',
      value: '7,100',
      change: '+15.3%',
      isPositive: true,
      icon: Users,
      description: 'Unique visitors this month'
    },
    {
      title: 'Page Views',
      value: '24,580',
      change: '+8.7%',
      isPositive: true,
      icon: Eye,
      description: 'Total page views'
    },
    {
      title: 'Conversion Rate',
      value: '4.2%',
      change: '+0.8%',
      isPositive: true,
      icon: MousePointer,
      description: 'Visitor to lead conversion'
    },
    {
      title: 'Revenue Attribution',
      value: '$41,000',
      change: '+12.5%',
      isPositive: true,
      icon: DollarSign,
      description: 'Revenue from marketing'
    },
    {
      title: 'Avg. Session Duration',
      value: '3m 42s',
      change: '-5.2%',
      isPositive: false,
      icon: Globe,
      description: 'Time spent on site'
    },
    {
      title: 'Bounce Rate',
      value: '45.2%',
      change: '-2.1%',
      isPositive: true,
      icon: TrendingDown,
      description: 'Visitors leaving immediately'
    }
  ];

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Marketing Analytics</h1>
          <p className="text-muted-foreground">
            Track and analyze marketing performance metrics
          </p>
        </div>
        <div className="flex gap-2">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-[150px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="last-7-days">Last 7 days</SelectItem>
              <SelectItem value="last-30-days">Last 30 days</SelectItem>
              <SelectItem value="last-90-days">Last 90 days</SelectItem>
              <SelectItem value="last-year">Last year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline">
            <Calendar className="mr-2 h-4 w-4" />
            Export Report
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {keyMetrics.map((metric, index) => {
          const IconComponent = metric.icon;
          return (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
                <IconComponent className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metric.value}</div>
                <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                  {metric.isPositive ? (
                    <TrendingUp className="h-3 w-3 text-green-500" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500" />
                  )}
                  <span className={metric.isPositive ? 'text-green-500' : 'text-red-500'}>
                    {metric.change}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  {metric.description}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Analytics Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="traffic">Traffic</TabsTrigger>
          <TabsTrigger value="conversions">Conversions</TabsTrigger>
          <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
          <TabsTrigger value="content">Content</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Performance Trend */}
            <Card>
              <CardHeader>
                <CardTitle>Performance Trend</CardTitle>
                <CardDescription>Key metrics over time</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="visitors" stroke="#8884d8" strokeWidth={2} />
                    <Line type="monotone" dataKey="leads" stroke="#82ca9d" strokeWidth={2} />
                    <Line type="monotone" dataKey="conversions" stroke="#ffc658" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Traffic Sources */}
            <Card>
              <CardHeader>
                <CardTitle>Traffic Sources</CardTitle>
                <CardDescription>Visitor acquisition channels</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={channelData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {channelData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Conversion Funnel */}
          <Card>
            <CardHeader>
              <CardTitle>Conversion Funnel</CardTitle>
              <CardDescription>Visitor journey through your marketing funnel</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {conversionFunnelData.map((stage, index) => (
                  <div key={index} className="flex items-center space-x-4">
                    <div className="w-24 text-sm font-medium">{stage.stage}</div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-muted-foreground">
                          {stage.count.toLocaleString()} ({stage.percentage}%)
                        </span>
                      </div>
                      <Progress value={stage.percentage} className="h-2" />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="traffic" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Device Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle>Device Breakdown</CardTitle>
                <CardDescription>Sessions by device type</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {deviceData.map((device, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {device.device === 'Desktop' && <Monitor className="h-4 w-4" />}
                        {device.device === 'Mobile' && <Smartphone className="h-4 w-4" />}
                        {device.device === 'Tablet' && <Monitor className="h-4 w-4" />}
                        <span className="font-medium">{device.device}</span>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">{device.sessions.toLocaleString()}</div>
                        <div className="text-sm text-muted-foreground">{device.percentage}%</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Top Pages */}
            <Card>
              <CardHeader>
                <CardTitle>Top Performing Pages</CardTitle>
                <CardDescription>Pages with highest engagement</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {topPages.map((page, index) => (
                    <div key={index} className="flex items-center justify-between p-2 rounded border">
                      <div className="flex-1">
                        <div className="text-sm font-medium truncate">{page.page}</div>
                        <div className="text-xs text-muted-foreground">
                          {page.views} views • {page.conversions} conversions
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{page.conversionRate}%</div>
                        <div className="text-xs text-muted-foreground">conversion</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="conversions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Conversion Performance</CardTitle>
              <CardDescription>Track conversion rates and optimization opportunities</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="conversions" stackId="1" stroke="#8884d8" fill="#8884d8" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="campaigns" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Campaign Performance</CardTitle>
              <CardDescription>Advertising campaign metrics and ROI</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {campaignPerformance.map((campaign, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <h3 className="font-medium">{campaign.campaign}</h3>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                        <span>{campaign.impressions.toLocaleString()} impressions</span>
                        <span>•</span>
                        <span>{campaign.clicks.toLocaleString()} clicks</span>
                        <span>•</span>
                        <span>{campaign.ctr}% CTR</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">{campaign.conversions} conversions</div>
                      <div className="text-sm text-muted-foreground">${campaign.cost} spent</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="content" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Content Performance</CardTitle>
              <CardDescription>Most engaging content and pages</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topPages.map((page, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <h3 className="font-medium">{page.page}</h3>
                      <div className="text-sm text-muted-foreground">
                        {page.views} views this month
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">{page.conversionRate}%</div>
                      <div className="text-sm text-muted-foreground">conversion rate</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}