import { useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Quote, Plus, Filter, Search, DollarSign, FileText, Clock, CheckCircle, Download, Send } from 'lucide-react';

export function QuotationsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const quotations = [
    {
      id: 'Q-2024-001',
      title: 'Enterprise Software License',
      customer: 'Acme Corporation',
      contact: 'John Smith',
      amount: '$125,000',
      status: 'sent',
      validUntil: '2024-02-15',
      createdDate: '2024-01-15',
      sentDate: '2024-01-15',
      owner: 'Sarah Johnson',
      items: 5,
      discount: '10%'
    },
    {
      id: 'Q-2024-002',
      title: 'Cloud Migration Services',
      customer: 'TechStart Inc',
      contact: 'Lisa Chen',
      amount: '$85,000',
      status: 'approved',
      validUntil: '2024-03-01',
      createdDate: '2024-01-10',
      sentDate: '2024-01-12',
      owner: 'Mike Wilson',
      items: 8,
      discount: '5%'
    },
    {
      id: 'Q-2024-003',
      title: 'Consulting Package',
      customer: 'Global Solutions',
      contact: 'David Park',
      amount: '$45,000',
      status: 'draft',
      validUntil: '2024-04-15',
      createdDate: '2024-01-14',
      sentDate: null,
      owner: 'Emma Thompson',
      items: 3,
      discount: '0%'
    },
    {
      id: 'Q-2024-004',
      title: 'Annual Support Contract',
      customer: 'InnovateCo',
      contact: 'Robert Kim',
      amount: '$95,000',
      status: 'expired',
      validUntil: '2024-01-10',
      createdDate: '2023-12-15',
      sentDate: '2023-12-20',
      owner: 'Alex Rodriguez',
      items: 4,
      discount: '15%'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'bg-gray-100 text-gray-800';
      case 'sent': return 'bg-blue-100 text-blue-800';
      case 'approved': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'expired': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'draft': return <FileText className="w-4 h-4" />;
      case 'sent': return <Send className="w-4 h-4" />;
      case 'approved': return <CheckCircle className="w-4 h-4" />;
      case 'expired': return <Clock className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  const filteredQuotations = quotations.filter(quote => {
    const matchesSearch = quote.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         quote.customer.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         quote.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || quote.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const totalValue = quotations.reduce((sum, quote) => sum + parseInt(quote.amount.replace(/[$,]/g, '')), 0);
  const approvedValue = quotations
    .filter(quote => quote.status === 'approved')
    .reduce((sum, quote) => sum + parseInt(quote.amount.replace(/[$,]/g, '')), 0);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Quotations & Proposals</h1>
          <p className="text-muted-foreground">Create, manage, and track sales quotations and proposals</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Templates</Button>
          <Button variant="outline">Approval Queue</Button>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Create Quote
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Quote className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Quotes</p>
              <p className="text-xl font-semibold">247</p>
              <p className="text-xs text-green-600">+18 this month</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <DollarSign className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Value</p>
              <p className="text-xl font-semibold">${(totalValue / 1000).toFixed(0)}K</p>
              <p className="text-xs text-green-600">Pipeline value</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <CheckCircle className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Approved Value</p>
              <p className="text-xl font-semibold">${(approvedValue / 1000).toFixed(0)}K</p>
              <p className="text-xs text-green-600">Ready to invoice</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Clock className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Approval Rate</p>
              <p className="text-xl font-semibold">68.4%</p>
              <p className="text-xs text-green-600">+5.2% improvement</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Quote Status Overview */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Quote Status Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {[
            { status: 'Draft', count: 12, value: '$180K', color: 'bg-gray-50' },
            { status: 'Sent', count: 45, value: '$1.2M', color: 'bg-blue-50' },
            { status: 'Approved', count: 89, value: '$2.8M', color: 'bg-green-50' },
            { status: 'Rejected', count: 23, value: '$450K', color: 'bg-red-50' },
            { status: 'Expired', count: 8, value: '$125K', color: 'bg-orange-50' }
          ].map((item, index) => (
            <div key={index} className={`text-center p-4 ${item.color} rounded-lg border`}>
              <div className="text-2xl font-semibold">{item.count}</div>
              <div className="text-sm text-muted-foreground">{item.status}</div>
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
            placeholder="Search quotations..."
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
            <SelectItem value="draft">Draft</SelectItem>
            <SelectItem value="sent">Sent</SelectItem>
            <SelectItem value="approved">Approved</SelectItem>
            <SelectItem value="rejected">Rejected</SelectItem>
            <SelectItem value="expired">Expired</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Quotations Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Quote ID</TableHead>
              <TableHead>Title & Customer</TableHead>
              <TableHead>Amount</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Valid Until</TableHead>
              <TableHead>Owner</TableHead>
              <TableHead>Items</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredQuotations.map((quote) => (
              <TableRow key={quote.id}>
                <TableCell className="font-mono">{quote.id}</TableCell>
                <TableCell>
                  <div>
                    <div className="font-medium">{quote.title}</div>
                    <div className="text-sm text-muted-foreground">{quote.customer}</div>
                    <div className="text-xs text-muted-foreground">Contact: {quote.contact}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <div>
                    <div className="font-medium">{quote.amount}</div>
                    {quote.discount !== '0%' && (
                      <div className="text-sm text-green-600">Discount: {quote.discount}</div>
                    )}
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {getStatusIcon(quote.status)}
                    <Badge className={getStatusColor(quote.status)}>
                      {quote.status}
                    </Badge>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="text-sm">
                    <div>{quote.validUntil}</div>
                    {quote.sentDate && (
                      <div className="text-muted-foreground">Sent: {quote.sentDate}</div>
                    )}
                  </div>
                </TableCell>
                <TableCell>{quote.owner}</TableCell>
                <TableCell>
                  <div className="text-center">
                    <div className="font-medium">{quote.items}</div>
                    <div className="text-xs text-muted-foreground">items</div>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                      <Download className="w-3 h-3 mr-1" />
                      PDF
                    </Button>
                    <Button variant="outline" size="sm">Edit</Button>
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