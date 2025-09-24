import { useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Progress } from '../../components/ui/progress';
import { Target, Plus, Filter, Search, DollarSign, Calendar, TrendingUp, Users } from 'lucide-react';

export function OpportunitiesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStage, setFilterStage] = useState('all');

  const opportunities = [
    {
      id: 1,
      name: 'Enterprise Software License',
      company: 'Acme Corporation',
      value: '$125,000',
      stage: 'negotiation',
      probability: 85,
      closeDate: '2024-02-15',
      owner: 'John Doe',
      createdDate: '2023-12-01',
      lastActivity: '2024-01-15',
      source: 'Inbound'
    },
    {
      id: 2,
      name: 'Cloud Migration Project',
      company: 'TechStart Inc',
      value: '$85,000',
      stage: 'proposal',
      probability: 65,
      closeDate: '2024-03-01',
      owner: 'Sarah Smith',
      createdDate: '2024-01-05',
      lastActivity: '2024-01-14',
      source: 'Referral'
    },
    {
      id: 3,
      name: 'Consulting Services',
      company: 'Global Solutions',
      value: '$45,000',
      stage: 'qualification',
      probability: 40,
      closeDate: '2024-04-15',
      owner: 'Mike Johnson',
      createdDate: '2024-01-10',
      lastActivity: '2024-01-13',
      source: 'Cold Outreach'
    },
    {
      id: 4,
      name: 'Annual Support Contract',
      company: 'InnovateCo',
      value: '$95,000',
      stage: 'closed-won',
      probability: 100,
      closeDate: '2024-01-10',
      owner: 'Lisa Wilson',
      createdDate: '2023-11-15',
      lastActivity: '2024-01-10',
      source: 'Existing Customer'
    }
  ];

  const getStageColor = (stage: string) => {
    switch (stage) {
      case 'qualification': return 'bg-blue-100 text-blue-800';
      case 'proposal': return 'bg-yellow-100 text-yellow-800';
      case 'negotiation': return 'bg-orange-100 text-orange-800';
      case 'closed-won': return 'bg-green-100 text-green-800';
      case 'closed-lost': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getProbabilityColor = (probability: number) => {
    if (probability >= 80) return 'text-green-600';
    if (probability >= 60) return 'text-yellow-600';
    if (probability >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const filteredOpportunities = opportunities.filter(opportunity => {
    const matchesSearch = opportunity.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         opportunity.company.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStage === 'all' || opportunity.stage === filterStage;
    return matchesSearch && matchesFilter;
  });

  const totalValue = opportunities.reduce((sum, opp) => sum + parseInt(opp.value.replace(/[$,]/g, '')), 0);
  const wonValue = opportunities
    .filter(opp => opp.stage === 'closed-won')
    .reduce((sum, opp) => sum + parseInt(opp.value.replace(/[$,]/g, '')), 0);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Sales Opportunities</h1>
          <p className="text-muted-foreground">Track and manage sales opportunities through your pipeline</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Pipeline View</Button>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            New Opportunity
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Target className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Opportunities</p>
              <p className="text-xl font-semibold">147</p>
              <p className="text-xs text-green-600">+8 this month</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <DollarSign className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Pipeline Value</p>
              <p className="text-xl font-semibold">${(totalValue / 1000).toFixed(0)}K</p>
              <p className="text-xs text-green-600">+12% growth</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <TrendingUp className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Won This Month</p>
              <p className="text-xl font-semibold">${(wonValue / 1000).toFixed(0)}K</p>
              <p className="text-xs text-green-600">95% of target</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Calendar className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Avg. Deal Size</p>
              <p className="text-xl font-semibold">${(totalValue / opportunities.length / 1000).toFixed(0)}K</p>
              <p className="text-xs text-green-600">+5% increase</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Pipeline Overview */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Pipeline by Stage</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { stage: 'Qualification', count: 45, value: '$1.2M' },
            { stage: 'Proposal', count: 28, value: '$850K' },
            { stage: 'Negotiation', count: 15, value: '$675K' },
            { stage: 'Closing', count: 8, value: '$320K' }
          ].map((item, index) => (
            <div key={index} className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-semibold">{item.count}</div>
              <div className="text-sm text-muted-foreground">{item.stage}</div>
              <div className="text-sm font-medium mt-1">{item.value}</div>
            </div>
          ))}
        </div>
      </Card>

      {/* Filters and Search */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search opportunities..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={filterStage} onValueChange={setFilterStage}>
          <SelectTrigger className="w-[200px]">
            <Filter className="w-4 h-4 mr-2" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Stages</SelectItem>
            <SelectItem value="qualification">Qualification</SelectItem>
            <SelectItem value="proposal">Proposal</SelectItem>
            <SelectItem value="negotiation">Negotiation</SelectItem>
            <SelectItem value="closed-won">Closed Won</SelectItem>
            <SelectItem value="closed-lost">Closed Lost</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Opportunities Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Opportunity</TableHead>
              <TableHead>Company</TableHead>
              <TableHead>Value</TableHead>
              <TableHead>Stage</TableHead>
              <TableHead>Probability</TableHead>
              <TableHead>Close Date</TableHead>
              <TableHead>Owner</TableHead>
              <TableHead>Last Activity</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredOpportunities.map((opportunity) => (
              <TableRow key={opportunity.id}>
                <TableCell>
                  <div>
                    <div className="font-medium">{opportunity.name}</div>
                    <div className="text-sm text-muted-foreground">Source: {opportunity.source}</div>
                  </div>
                </TableCell>
                <TableCell className="font-medium">{opportunity.company}</TableCell>
                <TableCell className="font-medium">{opportunity.value}</TableCell>
                <TableCell>
                  <Badge className={getStageColor(opportunity.stage)}>
                    {opportunity.stage.replace('-', ' ')}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span className={`font-medium ${getProbabilityColor(opportunity.probability)}`}>
                      {opportunity.probability}%
                    </span>
                    <Progress value={opportunity.probability} className="h-2 w-16" />
                  </div>
                </TableCell>
                <TableCell>{opportunity.closeDate}</TableCell>
                <TableCell>{opportunity.owner}</TableCell>
                <TableCell>{opportunity.lastActivity}</TableCell>
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