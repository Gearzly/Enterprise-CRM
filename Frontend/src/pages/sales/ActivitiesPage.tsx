import { useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Calendar, Phone, Mail, Video, MessageSquare, Plus, Filter, Search } from 'lucide-react';

export function ActivitiesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const activities = [
    {
      id: 1,
      type: 'call',
      title: 'Follow-up call with John Smith',
      contact: 'John Smith - Acme Corp',
      date: '2024-01-15',
      time: '10:30 AM',
      status: 'completed',
      outcome: 'Interested in premium package'
    },
    {
      id: 2,
      type: 'email',
      title: 'Proposal sent to TechStart Inc',
      contact: 'Sarah Johnson - TechStart Inc',
      date: '2024-01-15',
      time: '2:15 PM',
      status: 'pending',
      outcome: 'Awaiting response'
    },
    {
      id: 3,
      type: 'meeting',
      title: 'Product demo presentation',
      contact: 'Mike Wilson - Global Solutions',
      date: '2024-01-16',
      time: '9:00 AM',
      status: 'scheduled',
      outcome: 'Demo scheduled'
    },
    {
      id: 4,
      type: 'video',
      title: 'Virtual consultation',
      contact: 'Lisa Chen - InnovateCo',
      date: '2024-01-16',
      time: '3:30 PM',
      status: 'scheduled',
      outcome: 'Initial consultation'
    }
  ];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'call': return <Phone className="w-4 h-4" />;
      case 'email': return <Mail className="w-4 h-4" />;
      case 'meeting': return <Calendar className="w-4 h-4" />;
      case 'video': return <Video className="w-4 h-4" />;
      default: return <MessageSquare className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'scheduled': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredActivities = activities.filter(activity => {
    const matchesSearch = activity.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         activity.contact.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || activity.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Sales Activities</h1>
          <p className="text-muted-foreground">Track and manage all sales-related activities</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          New Activity
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Calendar className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Activities</p>
              <p className="text-xl font-semibold">147</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <Phone className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Calls Today</p>
              <p className="text-xl font-semibold">12</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Mail className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Emails Sent</p>
              <p className="text-xl font-semibold">28</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Video className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Meetings</p>
              <p className="text-xl font-semibold">8</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Filters and Search */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search activities..."
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
            <SelectItem value="completed">Completed</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="scheduled">Scheduled</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Activities Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Type</TableHead>
              <TableHead>Activity</TableHead>
              <TableHead>Contact</TableHead>
              <TableHead>Date & Time</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Outcome</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredActivities.map((activity) => (
              <TableRow key={activity.id}>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {getTypeIcon(activity.type)}
                    <span className="capitalize">{activity.type}</span>
                  </div>
                </TableCell>
                <TableCell className="font-medium">{activity.title}</TableCell>
                <TableCell>{activity.contact}</TableCell>
                <TableCell>
                  <div>
                    <div>{activity.date}</div>
                    <div className="text-sm text-muted-foreground">{activity.time}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge className={getStatusColor(activity.status)}>
                    {activity.status}
                  </Badge>
                </TableCell>
                <TableCell>{activity.outcome}</TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Edit</Button>
                    <Button variant="outline" size="sm">View</Button>
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