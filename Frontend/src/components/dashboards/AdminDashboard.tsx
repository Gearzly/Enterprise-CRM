import { MetricsCard } from '../MetricsCard';
import { SalesChart } from '../SalesChart';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import { Badge } from '../ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Settings, Shield, Users, Database, DollarSign, TrendingUp } from 'lucide-react';
import { salesData, teamPerformance } from '../../data/mockData';

export function AdminDashboard() {
  const systemUsers = [
    { id: '1', name: 'John Doe', email: 'john@company.com', role: 'Sales Rep', status: 'active', lastLogin: '2 hours ago' },
    { id: '2', name: 'Sarah Wilson', email: 'sarah@company.com', role: 'Sales Manager', status: 'active', lastLogin: '1 day ago' },
    { id: '3', name: 'Mike Rodriguez', email: 'mike@company.com', role: 'Sales Rep', status: 'active', lastLogin: '3 hours ago' },
    { id: '4', name: 'Lisa Thompson', email: 'lisa@company.com', role: 'Sales Manager', status: 'inactive', lastLogin: '1 week ago' },
  ];

  const systemMetrics = [
    { title: 'Total Users', value: '24', change: '+2 this month', trend: 'up' as const },
    { title: 'System Uptime', value: '99.9%', change: 'Last 30 days', trend: 'up' as const },
    { title: 'Data Storage', value: '78%', change: 'of 500GB used', trend: 'neutral' as const },
    { title: 'Active Sessions', value: '18', change: 'Current users online', trend: 'neutral' as const },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Admin Dashboard</h1>
          <p className="text-muted-foreground">System administration and user management</p>
        </div>
        <Button>
          <Settings className="w-4 h-4 mr-2" />
          System Settings
        </Button>
      </div>

      {/* System Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {systemMetrics.map((metric, index) => (
          <MetricsCard
            key={index}
            title={metric.title}
            value={metric.value}
            change={metric.change}
            trend={metric.trend}
            icon={index === 0 ? <Users className="w-6 h-6" /> : 
                  index === 1 ? <Shield className="w-6 h-6" /> :
                  index === 2 ? <Database className="w-6 h-6" /> :
                  <TrendingUp className="w-6 h-6" />}
          />
        ))}
      </div>

      {/* Business Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricsCard
          title="Total Revenue"
          value="$2.4M"
          change="+24% from last quarter"
          trend="up"
          icon={<DollarSign className="w-6 h-6" />}
        />
        <MetricsCard
          title="Total Customers"
          value="342"
          change="+45 this month"
          trend="up"
          icon={<Users className="w-6 h-6" />}
        />
        <MetricsCard
          title="Conversion Rate"
          value="73%"
          change="+8% improvement"
          trend="up"
          icon={<TrendingUp className="w-6 h-6" />}
        />
        <MetricsCard
          title="Active Deals"
          value="89"
          change="15 closing this week"
          trend="neutral"
          icon={<Database className="w-6 h-6" />}
        />
      </div>

      {/* Revenue Chart */}
      <SalesChart
        title="Company Revenue Trend"
        type="line"
        data={salesData}
        dataKey="sales"
        xAxisKey="month"
      />

      {/* User Management */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">User Management</h3>
          <Button variant="outline">Add User</Button>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>User</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Last Login</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {systemUsers.map((user) => (
              <TableRow key={user.id}>
                <TableCell>
                  <div className="flex items-center gap-3">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback>
                        {user.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="font-medium">{user.name}</p>
                      <p className="text-sm text-muted-foreground">{user.email}</p>
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant="outline">{user.role}</Badge>
                </TableCell>
                <TableCell>
                  <Badge 
                    variant={user.status === 'active' ? 'default' : 'secondary'}
                    className={user.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}
                  >
                    {user.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-muted-foreground">{user.lastLogin}</TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Edit</Button>
                    <Button variant="outline" size="sm">Reset Password</Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Team Performance Overview */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Team Performance Overview</h3>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Team Member</TableHead>
              <TableHead>Deals Closed</TableHead>
              <TableHead>Revenue Generated</TableHead>
              <TableHead>Target Achievement</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {teamPerformance.map((member, index) => {
              const achievement = Math.round((member.revenue / member.target) * 100);
              return (
                <TableRow key={index}>
                  <TableCell className="font-medium">{member.name}</TableCell>
                  <TableCell>{member.deals}</TableCell>
                  <TableCell>${member.revenue.toLocaleString()}</TableCell>
                  <TableCell>
                    <Badge 
                      variant={achievement >= 100 ? 'default' : achievement >= 80 ? 'secondary' : 'outline'}
                      className={achievement >= 100 ? 'bg-green-100 text-green-800' : 
                                achievement >= 80 ? 'bg-yellow-100 text-yellow-800' : 
                                'bg-red-100 text-red-800'}
                    >
                      {achievement}%
                    </Badge>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
}