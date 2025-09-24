import { MetricsCard } from '../MetricsCard';
import { SalesChart } from '../SalesChart';
import { Card } from '../ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { DollarSign, Users, Target, TrendingUp } from 'lucide-react';
import { salesData, pipelineData, teamPerformance, recentDeals } from '../../data/mockData';

export function ManagerDashboard() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Manager Dashboard</h1>
          <p className="text-muted-foreground">Oversee team performance and pipeline management</p>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricsCard
          title="Team Revenue"
          value="$1.2M"
          change="+18% from last quarter"
          trend="up"
          icon={<DollarSign className="w-6 h-6" />}
        />
        <MetricsCard
          title="Total Customers"
          value="156"
          change="+23 this month"
          trend="up"
          icon={<Users className="w-6 h-6" />}
        />
        <MetricsCard
          title="Active Deals"
          value="42"
          change="8 closing this week"
          trend="neutral"
          icon={<Target className="w-6 h-6" />}
        />
        <MetricsCard
          title="Team Performance"
          value="92%"
          change="+7% vs target"
          trend="up"
          icon={<TrendingUp className="w-6 h-6" />}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SalesChart
          title="Team Sales Performance"
          type="line"
          data={salesData}
          dataKey="sales"
          xAxisKey="month"
        />
        <SalesChart
          title="Pipeline by Stage"
          type="bar"
          data={pipelineData}
          dataKey="count"
          xAxisKey="stage"
        />
      </div>

      {/* Team Performance Table */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Team Performance</h3>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Sales Rep</TableHead>
              <TableHead>Deals Closed</TableHead>
              <TableHead>Revenue</TableHead>
              <TableHead>Target</TableHead>
              <TableHead>Performance</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {teamPerformance.map((member, index) => {
              const performance = Math.round((member.revenue / member.target) * 100);
              return (
                <TableRow key={index}>
                  <TableCell className="font-medium">{member.name}</TableCell>
                  <TableCell>{member.deals}</TableCell>
                  <TableCell>${member.revenue.toLocaleString()}</TableCell>
                  <TableCell>${member.target.toLocaleString()}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Progress value={performance} className="w-16" />
                      <span className="text-sm">{performance}%</span>
                    </div>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Card>

      {/* Recent Deals */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">High-Value Deals</h3>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Deal Name</TableHead>
              <TableHead>Company</TableHead>
              <TableHead>Value</TableHead>
              <TableHead>Stage</TableHead>
              <TableHead>Probability</TableHead>
              <TableHead>Close Date</TableHead>
              <TableHead>Owner</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {recentDeals.map((deal) => (
              <TableRow key={deal.id}>
                <TableCell className="font-medium">{deal.name}</TableCell>
                <TableCell>{deal.company}</TableCell>
                <TableCell className="font-medium">{deal.value}</TableCell>
                <TableCell>
                  <Badge variant="outline">{deal.stage}</Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Progress value={deal.probability} className="w-16" />
                    <span className="text-sm">{deal.probability}%</span>
                  </div>
                </TableCell>
                <TableCell>{deal.closeDate}</TableCell>
                <TableCell>{deal.owner}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
}