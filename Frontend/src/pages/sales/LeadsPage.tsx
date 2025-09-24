import { useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Progress } from '../../components/ui/progress';
import { UserPlus, Plus, Filter, Search, TrendingUp, Users, Star, Target } from 'lucide-react';

interface LeadsPageProps {
  onNavigate?: (view: string, id?: string) => void;
}

export function LeadsPage({ onNavigate }: LeadsPageProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const leads = [
    {
      id: 1,
      name: 'Alexandra Rodriguez',
      email: 'alex.rodriguez@newtech.com',
      company: 'NewTech Solutions',
      source: 'Website',
      score: 85,
      status: 'hot',
      value: '$45,000',
      assignedTo: 'John Doe',
      createdDate: '2024-01-10',
      lastActivity: '2024-01-15'
    },
    {
      id: 2,
      name: 'David Park',
      email: 'david.park@startupco.com',
      company: 'StartupCo',
      source: 'LinkedIn',
      score: 72,
      status: 'warm',
      value: '$32,000',
      assignedTo: 'Sarah Smith',
      createdDate: '2024-01-12',
      lastActivity: '2024-01-14'
    },
    {
      id: 3,
      name: 'Emma Thompson',
      email: 'emma.t@enterprisecorp.com',
      company: 'Enterprise Corp',
      source: 'Referral',
      score: 95,
      status: 'hot',
      value: '$120,000',
      assignedTo: 'Mike Johnson',
      createdDate: '2024-01-08',
      lastActivity: '2024-01-15'
    },
    {
      id: 4,
      name: 'Robert Kim',
      email: 'robert.kim@smallbiz.com',
      company: 'Small Business Inc',
      source: 'Cold Outreach',
      score: 45,
      status: 'cold',
      value: '$15,000',
      assignedTo: 'Lisa Wilson',
      createdDate: '2024-01-14',
      lastActivity: '2024-01-14'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'hot': return 'bg-red-100 text-red-800';
      case 'warm': return 'bg-yellow-100 text-yellow-800';
      case 'cold': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || lead.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Lead Management</h1>
          <p className="text-muted-foreground">Capture, qualify, and nurture leads through your sales process</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Lead Scoring</Button>
          <Button onClick={() => onNavigate?.('sales/leads/create')}>
            <Plus className="w-4 h-4 mr-2" />
            Create Lead
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <UserPlus className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Leads</p>
              <p className="text-xl font-semibold">847</p>
              <p className="text-xs text-green-600">+12% this month</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-red-100 rounded-lg">
              <Target className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Hot Leads</p>
              <p className="text-xl font-semibold">89</p>
              <p className="text-xs text-green-600">+8% this week</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Conversion Rate</p>
              <p className="text-xl font-semibold">23.4%</p>
              <p className="text-xs text-green-600">+2.1% improvement</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Star className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Avg. Lead Score</p>
              <p className="text-xl font-semibold">67</p>
              <p className="text-xs text-green-600">+5 points</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Lead Score Distribution */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Lead Score Distribution</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm">Hot Leads (80-100)</span>
              <span className="text-sm font-medium">89 leads</span>
            </div>
            <Progress value={35} className="h-2" />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm">Warm Leads (60-79)</span>
              <span className="text-sm font-medium">234 leads</span>
            </div>
            <Progress value={45} className="h-2" />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm">Cold Leads (0-59)</span>
              <span className="text-sm font-medium">524 leads</span>
            </div>
            <Progress value={62} className="h-2" />
          </div>
        </div>
      </Card>

      {/* Filters and Search */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search leads..."
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
            <SelectItem value="hot">Hot Leads</SelectItem>
            <SelectItem value="warm">Warm Leads</SelectItem>
            <SelectItem value="cold">Cold Leads</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Leads Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Lead</TableHead>
              <TableHead>Company</TableHead>
              <TableHead>Source</TableHead>
              <TableHead>Score</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Value</TableHead>
              <TableHead>Assigned To</TableHead>
              <TableHead>Last Activity</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredLeads.map((lead) => (
              <TableRow key={lead.id}>
                <TableCell>
                  <div>
                    <div className="font-medium">{lead.name}</div>
                    <div className="text-sm text-muted-foreground">{lead.email}</div>
                  </div>
                </TableCell>
                <TableCell className="font-medium">{lead.company}</TableCell>
                <TableCell>{lead.source}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span className={`font-medium ${getScoreColor(lead.score)}`}>
                      {lead.score}
                    </span>
                    <Progress value={lead.score} className="h-2 w-16" />
                  </div>
                </TableCell>
                <TableCell>
                  <Badge className={getStatusColor(lead.status)}>
                    {lead.status}
                  </Badge>
                </TableCell>
                <TableCell className="font-medium">{lead.value}</TableCell>
                <TableCell>{lead.assignedTo}</TableCell>
                <TableCell>{lead.lastActivity}</TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Convert</Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => onNavigate?.('sales/leads/edit', lead.id.toString())}
                    >
                      Edit
                    </Button>
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