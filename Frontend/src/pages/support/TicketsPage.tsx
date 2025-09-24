import { useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { Ticket, Plus, Filter, Search, Clock, AlertTriangle, CheckCircle, XCircle, Users, MessageSquare } from 'lucide-react';

export function TicketsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPriority, setFilterPriority] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  const tickets = [
    {
      id: 'T-001',
      title: 'Login issues with new mobile app',
      customer: 'John Smith',
      customerEmail: 'john.smith@acmecorp.com',
      priority: 'high',
      status: 'open',
      assignee: 'Sarah Johnson',
      category: 'Technical',
      createdDate: '2024-01-15',
      lastUpdate: '2024-01-15 2:30 PM',
      responseTime: '15 mins',
      description: 'User unable to login using Face ID on iOS app'
    },
    {
      id: 'T-002',
      title: 'Billing discrepancy in invoice #12345',
      customer: 'Lisa Chen',
      customerEmail: 'lisa.chen@innovateco.com',
      priority: 'medium',
      status: 'in-progress',
      assignee: 'Mike Wilson',
      category: 'Billing',
      createdDate: '2024-01-14',
      lastUpdate: '2024-01-15 10:15 AM',
      responseTime: '1 hour',
      description: 'Customer questioning charges on recent invoice'
    },
    {
      id: 'T-003',
      title: 'Feature request: Dark mode support',
      customer: 'David Park',
      customerEmail: 'david.park@techstart.com',
      priority: 'low',
      status: 'resolved',
      assignee: 'Emma Thompson',
      category: 'Feature Request',
      createdDate: '2024-01-10',
      lastUpdate: '2024-01-14 4:45 PM',
      responseTime: '30 mins',
      description: 'Customer requesting dark mode theme option'
    },
    {
      id: 'T-004',
      title: 'Data export not working',
      customer: 'Robert Kim',
      customerEmail: 'robert.kim@smallbiz.com',
      priority: 'high',
      status: 'escalated',
      assignee: 'Alex Rodriguez',
      category: 'Technical',
      createdDate: '2024-01-13',
      lastUpdate: '2024-01-15 9:20 AM',
      responseTime: '5 mins',
      description: 'Export functionality throwing error on large datasets'
    }
  ];

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-blue-100 text-blue-800';
      case 'in-progress': return 'bg-orange-100 text-orange-800';
      case 'resolved': return 'bg-green-100 text-green-800';
      case 'escalated': return 'bg-red-100 text-red-800';
      case 'closed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open': return <Clock className="w-4 h-4" />;
      case 'in-progress': return <MessageSquare className="w-4 h-4" />;
      case 'resolved': return <CheckCircle className="w-4 h-4" />;
      case 'escalated': return <AlertTriangle className="w-4 h-4" />;
      case 'closed': return <XCircle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const filteredTickets = tickets.filter(ticket => {
    const matchesSearch = ticket.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         ticket.customer.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         ticket.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPriority = filterPriority === 'all' || ticket.priority === filterPriority;
    const matchesStatus = filterStatus === 'all' || ticket.status === filterStatus;
    return matchesSearch && matchesPriority && matchesStatus;
  });

  const ticketCounts = {
    open: tickets.filter(t => t.status === 'open').length,
    inProgress: tickets.filter(t => t.status === 'in-progress').length,
    resolved: tickets.filter(t => t.status === 'resolved').length,
    escalated: tickets.filter(t => t.status === 'escalated').length
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Support Tickets</h1>
          <p className="text-muted-foreground">Manage customer support tickets and issues</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Escalation Rules</Button>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            New Ticket
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Ticket className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Open Tickets</p>
              <p className="text-xl font-semibold">{ticketCounts.open}</p>
              <p className="text-xs text-orange-600">Needs attention</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <MessageSquare className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">In Progress</p>
              <p className="text-xl font-semibold">{ticketCounts.inProgress}</p>
              <p className="text-xs text-blue-600">Being worked on</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-red-100 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Escalated</p>
              <p className="text-xl font-semibold">{ticketCounts.escalated}</p>
              <p className="text-xs text-red-600">Urgent attention</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Resolved Today</p>
              <p className="text-xl font-semibold">12</p>
              <p className="text-xs text-green-600">+5 from yesterday</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Response Time Metrics */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Response Time Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-muted rounded-lg">
            <div className="text-2xl font-semibold text-green-600">4.2 hrs</div>
            <div className="text-sm text-muted-foreground">Average First Response</div>
            <div className="text-xs text-green-600 mt-1">↓ 15% from last week</div>
          </div>
          <div className="text-center p-4 bg-muted rounded-lg">
            <div className="text-2xl font-semibold text-blue-600">18.5 hrs</div>
            <div className="text-sm text-muted-foreground">Average Resolution Time</div>
            <div className="text-xs text-green-600 mt-1">↓ 8% improvement</div>
          </div>
          <div className="text-center p-4 bg-muted rounded-lg">
            <div className="text-2xl font-semibold text-purple-600">94.2%</div>
            <div className="text-sm text-muted-foreground">Customer Satisfaction</div>
            <div className="text-xs text-green-600 mt-1">↑ 2% increase</div>
          </div>
        </div>
      </Card>

      {/* Filters and Search */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search tickets..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={filterPriority} onValueChange={setFilterPriority}>
          <SelectTrigger className="w-[150px]">
            <Filter className="w-4 h-4 mr-2" />
            <SelectValue placeholder="Priority" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Priority</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="low">Low</SelectItem>
          </SelectContent>
        </Select>
        <Select value={filterStatus} onValueChange={setFilterStatus}>
          <SelectTrigger className="w-[150px]">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="open">Open</SelectItem>
            <SelectItem value="in-progress">In Progress</SelectItem>
            <SelectItem value="resolved">Resolved</SelectItem>
            <SelectItem value="escalated">Escalated</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Tickets Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ticket ID</TableHead>
              <TableHead>Title & Customer</TableHead>
              <TableHead>Priority</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Assignee</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Last Update</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredTickets.map((ticket) => (
              <TableRow key={ticket.id}>
                <TableCell className="font-mono">{ticket.id}</TableCell>
                <TableCell>
                  <div>
                    <div className="font-medium">{ticket.title}</div>
                    <div className="text-sm text-muted-foreground">{ticket.customer}</div>
                    <div className="text-xs text-muted-foreground">{ticket.customerEmail}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge className={getPriorityColor(ticket.priority)}>
                    {ticket.priority}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {getStatusIcon(ticket.status)}
                    <Badge className={getStatusColor(ticket.status)}>
                      {ticket.status.replace('-', ' ')}
                    </Badge>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Avatar className="w-6 h-6">
                      <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${ticket.assignee}`} />
                      <AvatarFallback>{ticket.assignee.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <span className="text-sm">{ticket.assignee}</span>
                  </div>
                </TableCell>
                <TableCell>{ticket.category}</TableCell>
                <TableCell>
                  <div className="text-sm">
                    <div>{ticket.lastUpdate}</div>
                    <div className="text-muted-foreground">Response: {ticket.responseTime}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">View</Button>
                    <Button variant="outline" size="sm">Reply</Button>
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