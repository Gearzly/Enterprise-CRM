import { MetricsCard } from '../MetricsCard';
import { SalesChart } from '../SalesChart';
import { CustomerTable } from '../CustomerTable';
import { ActivityFeed } from '../ActivityFeed';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Card } from '../ui/card';
import { DollarSign, Users, Target, TrendingUp, Plus, Calendar, Bell, Filter, Download, RefreshCw } from 'lucide-react';
import { salesData, customers, activities } from '../../data/mockData';
import { motion } from 'motion/react';
import { useState } from 'react';

export function SalesRepDashboard() {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const myCustomers = customers.slice(0, 3); // Show only first 3 customers for sales rep
  const myActivities = activities.slice(0, 4); // Show recent activities
  
  const currentTime = new Date().toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
  
  const currentDate = new Date().toLocaleDateString('en-US', { 
    weekday: 'long',
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  const handleRefresh = async () => {
    setIsRefreshing(true);
    // Simulate data refresh
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsRefreshing(false);
  };

  return (
    <div className="p-6 space-y-8 bg-gradient-to-br from-background to-muted/20 min-h-screen">
      {/* Enhanced Header */}
      <motion.div 
        className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              Sales Dashboard
            </h1>
            <Badge variant="outline" className="text-xs">
              Live
            </Badge>
          </div>
          <div className="flex items-center gap-4 text-muted-foreground">
            <p>Welcome back! Here's your performance overview</p>
            <div className="flex items-center gap-2 text-sm">
              <Calendar className="w-4 h-4" />
              <span>{currentDate}</span>
              <span className="text-xs">•</span>
              <span>{currentTime}</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={handleRefresh} disabled={isRefreshing}>
            <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button variant="outline" size="sm">
            <Filter className="w-4 h-4 mr-2" />
            Filter
          </Button>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button size="sm">
            <Plus className="w-4 h-4 mr-2" />
            Quick Action
          </Button>
        </div>
      </motion.div>

      {/* Metrics Cards */}
      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <MetricsCard
          title="Monthly Revenue"
          value="$67,000"
          change="+12% from last month"
          trend="up"
          percentage="12"
          icon={<DollarSign className="w-6 h-6" />}
          isLoading={isRefreshing}
        />
        <MetricsCard
          title="Active Customers"
          value="24"
          change="+3 new this month"
          trend="up"
          percentage="8"
          icon={<Users className="w-6 h-6" />}
          isLoading={isRefreshing}
        />
        <MetricsCard
          title="Deals in Pipeline"
          value="8"
          change="2 closing this week"
          trend="neutral"
          percentage="25"
          icon={<Target className="w-6 h-6" />}
          isLoading={isRefreshing}
        />
        <MetricsCard
          title="Conversion Rate"
          value="68%"
          change="+5% from last month"
          trend="up"
          percentage="68"
          icon={<TrendingUp className="w-6 h-6" />}
          isLoading={isRefreshing}
        />
      </motion.div>

      {/* Charts and Activity Feed */}
      <motion.div 
        className="grid grid-cols-1 xl:grid-cols-3 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <div className="xl:col-span-2">
          <SalesChart
            title="Monthly Sales Performance"
            type="line"
            data={salesData}
            dataKey="sales"
            xAxisKey="month"
          />
        </div>
        <div className="xl:col-span-1">
          <ActivityFeed title="Recent Activities" activities={myActivities} />
        </div>
      </motion.div>

      {/* Enhanced Customer Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold">My Active Customers</h3>
              <p className="text-sm text-muted-foreground">Your most important customer relationships</p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm">
                View All
              </Button>
              <Button size="sm">
                <Plus className="w-4 h-4 mr-2" />
                Add Customer
              </Button>
            </div>
          </div>
          <CustomerTable customers={myCustomers} />
        </Card>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button variant="outline" className="h-20 flex-col gap-2">
              <Plus className="w-6 h-6" />
              <span className="text-sm">New Lead</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col gap-2">
              <Target className="w-6 h-6" />
              <span className="text-sm">New Deal</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col gap-2">
              <Calendar className="w-6 h-6" />
              <span className="text-sm">Schedule Meeting</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col gap-2">
              <Bell className="w-6 h-6" />
              <span className="text-sm">Follow Up</span>
            </Button>
          </div>
        </Card>
      </motion.div>
    </div>
  );
}