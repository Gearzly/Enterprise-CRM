import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Plus, Search, Filter, Mail, Phone, MapPin, Building, User, TrendingUp } from 'lucide-react';
import { useState } from 'react';

export function LeadsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedSource, setSelectedSource] = useState('all');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const leads = [
    {
      id: 1,
      name: 'Jennifer Wilson',
      email: 'jennifer.wilson@techcorp.com',
      phone: '+1 (555) 123-4567',
      company: 'TechCorp Solutions',
      position: 'Marketing Director',
      status: 'New',
      source: 'Website',
      score: 85,
      location: 'San Francisco, CA',
      lastActivity: '2024-01-15',
      notes: 'Interested in enterprise package'
    },
    {
      id: 2,
      name: 'Michael Rodriguez',
      email: 'michael.r@innovate.io',
      phone: '+1 (555) 234-5678',
      company: 'Innovate.io',
      position: 'CEO',
      status: 'Qualified',
      source: 'LinkedIn',
      score: 92,
      location: 'Austin, TX',
      lastActivity: '2024-01-14',
      notes: 'Ready for demo, budget approved'
    },
    {
      id: 3,
      name: 'Sarah Chen',
      email: 'sarah.chen@datatech.com',
      phone: '+1 (555) 345-6789',
      company: 'DataTech Analytics',
      position: 'VP of Operations',
      status: 'Contacted',
      source: 'Google Ads',
      score: 78,
      location: 'Seattle, WA',
      lastActivity: '2024-01-13',
      notes: 'Evaluating multiple solutions'
    },
    {
      id: 4,
      name: 'David Thompson',
      email: 'david.t@futuresoft.net',
      phone: '+1 (555) 456-7890',
      company: 'FutureSoft',
      position: 'CTO',
      status: 'Nurturing',
      source: 'Referral',
      score: 88,
      location: 'Boston, MA',
      lastActivity: '2024-01-12',
      notes: 'Technical evaluation in progress'
    },
    {
      id: 5,
      name: 'Lisa Park',
      email: 'lisa.park@growthco.com',
      phone: '+1 (555) 567-8901',
      company: 'GrowthCo',
      position: 'Head of Marketing',
      status: 'Cold',
      source: 'Trade Show',
      score: 65,
      location: 'Chicago, IL',
      lastActivity: '2024-01-10',
      notes: 'Initial contact made'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'New': return 'bg-blue-500';
      case 'Qualified': return 'bg-green-500';
      case 'Contacted': return 'bg-yellow-500';
      case 'Nurturing': return 'bg-purple-500';
      case 'Cold': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-yellow-500';
    return 'text-red-500';
  };

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = selectedStatus === 'all' || lead.status === selectedStatus;
    const matchesSource = selectedSource === 'all' || lead.source === selectedSource;
    
    return matchesSearch && matchesStatus && matchesSource;
  });

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Marketing Leads</h1>
          <p className="text-muted-foreground">
            Manage and nurture marketing qualified leads
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Filter className="mr-2 h-4 w-4" />
            Export
          </Button>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Add Lead
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Add New Lead</DialogTitle>
                <DialogDescription>
                  Add a new marketing lead to your pipeline
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">Name</Label>
                  <Input id="name" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="email" className="text-right">Email</Label>
                  <Input id="email" type="email" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="company" className="text-right">Company</Label>
                  <Input id="company" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="source" className="text-right">Source</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select source" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="website">Website</SelectItem>
                      <SelectItem value="linkedin">LinkedIn</SelectItem>
                      <SelectItem value="google-ads">Google Ads</SelectItem>
                      <SelectItem value="referral">Referral</SelectItem>
                      <SelectItem value="trade-show">Trade Show</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="notes" className="text-right">Notes</Label>
                  <Textarea id="notes" className="col-span-3" />
                </div>
              </div>
              <DialogFooter>
                <Button type="submit" onClick={() => setIsCreateDialogOpen(false)}>
                  Add Lead
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Lead Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Leads</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{leads.length}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+12%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Qualified Leads</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {leads.filter(lead => lead.status === 'Qualified').length}
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+8%</span> conversion rate
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Score</CardTitle>
            <Building className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(leads.reduce((sum, lead) => sum + lead.score, 0) / leads.length)}
            </div>
            <p className="text-xs text-muted-foreground">
              Lead quality score
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Top Source</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Website</div>
            <p className="text-xs text-muted-foreground">
              40% of all leads
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  placeholder="Search leads..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Select value={selectedStatus} onValueChange={setSelectedStatus}>
              <SelectTrigger className="w-[150px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="New">New</SelectItem>
                <SelectItem value="Qualified">Qualified</SelectItem>
                <SelectItem value="Contacted">Contacted</SelectItem>
                <SelectItem value="Nurturing">Nurturing</SelectItem>
                <SelectItem value="Cold">Cold</SelectItem>
              </SelectContent>
            </Select>
            <Select value={selectedSource} onValueChange={setSelectedSource}>
              <SelectTrigger className="w-[150px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Sources</SelectItem>
                <SelectItem value="Website">Website</SelectItem>
                <SelectItem value="LinkedIn">LinkedIn</SelectItem>
                <SelectItem value="Google Ads">Google Ads</SelectItem>
                <SelectItem value="Referral">Referral</SelectItem>
                <SelectItem value="Trade Show">Trade Show</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Leads Table */}
      <Card>
        <CardHeader>
          <CardTitle>Marketing Leads</CardTitle>
          <CardDescription>
            {filteredLeads.length} leads found
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Lead</TableHead>
                <TableHead>Company</TableHead>
                <TableHead>Contact</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Source</TableHead>
                <TableHead>Score</TableHead>
                <TableHead>Last Activity</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLeads.map((lead) => (
                <TableRow key={lead.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium">{lead.name}</div>
                      <div className="text-sm text-muted-foreground">{lead.position}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">{lead.company}</div>
                      <div className="text-sm text-muted-foreground">{lead.location}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 text-sm">
                        <Mail className="h-3 w-3" />
                        {lead.email}
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <Phone className="h-3 w-3" />
                        {lead.phone}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(lead.status)}>
                      {lead.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{lead.source}</TableCell>
                  <TableCell>
                    <span className={`font-medium ${getScoreColor(lead.score)}`}>
                      {lead.score}
                    </span>
                  </TableCell>
                  <TableCell>{lead.lastActivity}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="outline" size="sm">
                        Edit
                      </Button>
                      <Button variant="outline" size="sm">
                        Convert
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}