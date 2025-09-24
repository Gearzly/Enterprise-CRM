import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Textarea } from '../../components/ui/textarea';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Label } from '../../components/ui/label';
import { Switch } from '../../components/ui/switch';
import { Progress } from '../../components/ui/progress';
import { Checkbox } from '../../components/ui/checkbox';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { 
  Users, Plus, Filter, Search, Eye, Edit, Trash2, Star, 
  Clock, User, Tag, Globe, FileText, BarChart3, 
  TrendingUp, Share2, Copy, Archive, CheckCircle,
  AlertCircle, XCircle, PlayCircle, PauseCircle, RefreshCw,
  Zap, Settings, Download, Upload, PieChart, Activity,
  MapPin, DollarSign, ShoppingCart, Mail, Phone, Smartphone,
  Video, Mic, Camera, Monitor, Headphones, MessageSquare,
  ExternalLink, QrCode, Ticket, Gift, Award, Target,
  Handshake, Building, Calendar, CreditCard, Briefcase,
  Network, Shield, Key, Lock, Unlock, UserCheck,
  TrendingDown, AlertTriangle, Info, Heart, ThumbsUp,
  FileCheck, FileX, FilePlus, Folder, FolderOpen,
  Link, Unlink, Send, Inbox, Outbox, Bell, BellOff
} from 'lucide-react';

interface Partner {
  id: number;
  name: string;
  company: string;
  email: string;
  phone: string;
  website: string;
  logo?: string;
  type: 'reseller' | 'distributor' | 'technology' | 'referral' | 'strategic' | 'channel';
  tier: 'bronze' | 'silver' | 'gold' | 'platinum' | 'diamond';
  status: 'active' | 'inactive' | 'pending' | 'suspended' | 'terminated';
  onboardingStatus: 'not-started' | 'in-progress' | 'completed' | 'on-hold';
  joinDate: string;
  lastActivity: string;
  region: string;
  country: string;
  industry: string;
  revenue: number;
  deals: number;
  leads: number;
  commissionRate: number;
  totalCommission: number;
  certifications: string[];
  tags: string[];
  contactPerson: string;
  accountManager: string;
  performanceScore: number;
  satisfactionScore: number;
  contractEndDate?: string;
  notes: string;
}

interface PartnerProgram {
  id: number;
  name: string;
  description: string;
  type: 'certification' | 'training' | 'incentive' | 'marketing' | 'technical';
  status: 'active' | 'inactive' | 'draft';
  startDate: string;
  endDate?: string;
  participants: number;
  completionRate: number;
  budget: number;
  spent: number;
  roi: number;
  requirements: string[];
  benefits: string[];
  manager: string;
}

export function PartnersPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [filterTier, setFilterTier] = useState('all');
  const [selectedPartner, setSelectedPartner] = useState<Partner | null>(null);
  const [isCreatePartnerDialogOpen, setIsCreatePartnerDialogOpen] = useState(false);
  const [isCreateProgramDialogOpen, setIsCreateProgramDialogOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('partners');

  const partners: Partner[] = [
    {
      id: 1,
      name: 'John Smith',
      company: 'TechSolutions Inc.',
      email: 'john.smith@techsolutions.com',
      phone: '+1-555-0123',
      website: 'https://techsolutions.com',
      logo: '/api/placeholder/40/40',
      type: 'reseller',
      tier: 'gold',
      status: 'active',
      onboardingStatus: 'completed',
      joinDate: '2023-06-15',
      lastActivity: '2024-02-01',
      region: 'North America',
      country: 'United States',
      industry: 'Technology',
      revenue: 125000,
      deals: 15,
      leads: 45,
      commissionRate: 15,
      totalCommission: 18750,
      certifications: ['Sales Certified', 'Technical Certified'],
      tags: ['high-performer', 'strategic'],
      contactPerson: 'John Smith',
      accountManager: 'Sarah Johnson',
      performanceScore: 92,
      satisfactionScore: 4.8,
      contractEndDate: '2024-12-31',
      notes: 'Excellent partner with strong technical expertise'
    },
    {
      id: 2,
      name: 'Maria Garcia',
      company: 'Global Distributors Ltd.',
      email: 'maria@globaldist.com',
      phone: '+44-20-7123-4567',
      website: 'https://globaldist.com',
      type: 'distributor',
      tier: 'platinum',
      status: 'active',
      onboardingStatus: 'completed',
      joinDate: '2022-03-10',
      lastActivity: '2024-01-28',
      region: 'Europe',
      country: 'United Kingdom',
      industry: 'Distribution',
      revenue: 350000,
      deals: 42,
      leads: 128,
      commissionRate: 12,
      totalCommission: 42000,
      certifications: ['Sales Certified', 'Technical Certified', 'Advanced Partner'],
      tags: ['top-performer', 'enterprise'],
      contactPerson: 'Maria Garcia',
      accountManager: 'Mike Chen',
      performanceScore: 96,
      satisfactionScore: 4.9,
      contractEndDate: '2025-03-10',
      notes: 'Top-tier partner with excellent market reach'
    },
    {
      id: 3,
      name: 'David Kim',
      company: 'Innovation Partners',
      email: 'david@innovationpartners.com',
      phone: '+82-2-1234-5678',
      website: 'https://innovationpartners.com',
      type: 'technology',
      tier: 'silver',
      status: 'active',
      onboardingStatus: 'in-progress',
      joinDate: '2024-01-15',
      lastActivity: '2024-01-30',
      region: 'Asia Pacific',
      country: 'South Korea',
      industry: 'Technology',
      revenue: 75000,
      deals: 8,
      leads: 22,
      commissionRate: 18,
      totalCommission: 13500,
      certifications: ['Technical Certified'],
      tags: ['new-partner', 'technology'],
      contactPerson: 'David Kim',
      accountManager: 'Emily Rodriguez',
      performanceScore: 78,
      satisfactionScore: 4.5,
      notes: 'Promising new technology partner'
    },
    {
      id: 4,
      name: 'Lisa Wang',
      company: 'Strategic Consulting Group',
      email: 'lisa@strategiccg.com',
      phone: '+1-415-555-0199',
      website: 'https://strategiccg.com',
      type: 'strategic',
      tier: 'diamond',
      status: 'active',
      onboardingStatus: 'completed',
      joinDate: '2021-09-20',
      lastActivity: '2024-02-02',
      region: 'North America',
      country: 'United States',
      industry: 'Consulting',
      revenue: 500000,
      deals: 28,
      leads: 85,
      commissionRate: 10,
      totalCommission: 50000,
      certifications: ['Sales Certified', 'Technical Certified', 'Advanced Partner', 'Strategic Partner'],
      tags: ['strategic', 'enterprise', 'consulting'],
      contactPerson: 'Lisa Wang',
      accountManager: 'David Park',
      performanceScore: 98,
      satisfactionScore: 5.0,
      contractEndDate: '2026-09-20',
      notes: 'Premier strategic partner with exceptional results'
    },
    {
      id: 5,
      name: 'Ahmed Hassan',
      company: 'Middle East Solutions',
      email: 'ahmed@mesolutions.com',
      phone: '+971-4-123-4567',
      website: 'https://mesolutions.com',
      type: 'referral',
      tier: 'bronze',
      status: 'pending',
      onboardingStatus: 'not-started',
      joinDate: '2024-02-01',
      lastActivity: '2024-02-01',
      region: 'Middle East',
      country: 'United Arab Emirates',
      industry: 'Technology',
      revenue: 0,
      deals: 0,
      leads: 3,
      commissionRate: 20,
      totalCommission: 0,
      certifications: [],
      tags: ['new-partner', 'pending'],
      contactPerson: 'Ahmed Hassan',
      accountManager: 'Sarah Johnson',
      performanceScore: 0,
      satisfactionScore: 0,
      notes: 'New partner application under review'
    }
  ];

  const programs: PartnerProgram[] = [
    {
      id: 1,
      name: 'Partner Certification Program',
      description: 'Comprehensive certification program for new partners',
      type: 'certification',
      status: 'active',
      startDate: '2024-01-01',
      endDate: '2024-12-31',
      participants: 25,
      completionRate: 68,
      budget: 50000,
      spent: 32000,
      roi: 245,
      requirements: ['Complete training modules', 'Pass certification exam', 'Complete 3 deals'],
      benefits: ['Higher commission rates', 'Marketing support', 'Priority support'],
      manager: 'Sarah Johnson'
    },
    {
      id: 2,
      name: 'Q1 Sales Incentive',
      description: 'Quarterly sales incentive program for top performers',
      type: 'incentive',
      status: 'active',
      startDate: '2024-01-01',
      endDate: '2024-03-31',
      participants: 15,
      completionRate: 87,
      budget: 75000,
      spent: 45000,
      roi: 320,
      requirements: ['Achieve 150% of quota', 'Maintain customer satisfaction >4.5'],
      benefits: ['Bonus commission', 'Recognition awards', 'Exclusive events'],
      manager: 'Mike Chen'
    },
    {
      id: 3,
      name: 'Technical Training Series',
      description: 'Advanced technical training for technology partners',
      type: 'training',
      status: 'active',
      startDate: '2024-02-01',
      endDate: '2024-05-31',
      participants: 12,
      completionRate: 42,
      budget: 30000,
      spent: 18000,
      roi: 180,
      requirements: ['Technical background', 'Complete prerequisites', 'Hands-on projects'],
      benefits: ['Technical certification', 'Access to beta features', 'Technical support'],
      manager: 'Emily Rodriguez'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'inactive': return 'bg-gray-100 text-gray-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'suspended': return 'bg-orange-100 text-orange-800';
      case 'terminated': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'bronze': return 'bg-amber-100 text-amber-800';
      case 'silver': return 'bg-gray-100 text-gray-800';
      case 'gold': return 'bg-yellow-100 text-yellow-800';
      case 'platinum': return 'bg-blue-100 text-blue-800';
      case 'diamond': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getOnboardingStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in-progress': return 'bg-blue-100 text-blue-800';
      case 'on-hold': return 'bg-yellow-100 text-yellow-800';
      case 'not-started': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'reseller': return <ShoppingCart className="h-4 w-4" />;
      case 'distributor': return <Network className="h-4 w-4" />;
      case 'technology': return <Monitor className="h-4 w-4" />;
      case 'referral': return <Share2 className="h-4 w-4" />;
      case 'strategic': return <Target className="h-4 w-4" />;
      case 'channel': return <Users className="h-4 w-4" />;
      default: return <Handshake className="h-4 w-4" />;
    }
  };

  const filteredPartners = partners.filter(partner => {
    const matchesSearch = partner.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         partner.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         partner.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         partner.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = filterStatus === 'all' || partner.status === filterStatus;
    const matchesType = filterType === 'all' || partner.type === filterType;
    const matchesTier = filterTier === 'all' || partner.tier === filterTier;
    return matchesSearch && matchesStatus && matchesType && matchesTier;
  });

  const partnerStats = {
    total: partners.length,
    active: partners.filter(p => p.status === 'active').length,
    totalRevenue: partners.reduce((sum, p) => sum + p.revenue, 0),
    totalCommission: partners.reduce((sum, p) => sum + p.totalCommission, 0),
    avgPerformance: partners.reduce((sum, p) => sum + p.performanceScore, 0) / partners.length
  };

  const CreatePartnerDialog = () => (
    <Dialog open={isCreatePartnerDialogOpen} onOpenChange={setIsCreatePartnerDialogOpen}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Add New Partner</DialogTitle>
          <DialogDescription>
            Onboard a new partner to your partner program.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-6 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="partnerName">Contact Name</Label>
              <Input id="partnerName" placeholder="Enter contact name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="company">Company Name</Label>
              <Input id="company" placeholder="Enter company name" />
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <Input id="email" type="email" placeholder="Enter email address" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number</Label>
              <Input id="phone" placeholder="Enter phone number" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="website">Website</Label>
              <Input id="website" placeholder="https://example.com" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="partnerType">Partner Type</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="reseller">Reseller</SelectItem>
                  <SelectItem value="distributor">Distributor</SelectItem>
                  <SelectItem value="technology">Technology Partner</SelectItem>
                  <SelectItem value="referral">Referral Partner</SelectItem>
                  <SelectItem value="strategic">Strategic Partner</SelectItem>
                  <SelectItem value="channel">Channel Partner</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="region">Region</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select region" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="north-america">North America</SelectItem>
                  <SelectItem value="europe">Europe</SelectItem>
                  <SelectItem value="asia-pacific">Asia Pacific</SelectItem>
                  <SelectItem value="latin-america">Latin America</SelectItem>
                  <SelectItem value="middle-east">Middle East</SelectItem>
                  <SelectItem value="africa">Africa</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="country">Country</Label>
              <Input id="country" placeholder="Enter country" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="industry">Industry</Label>
              <Input id="industry" placeholder="Enter industry" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="commissionRate">Commission Rate (%)</Label>
              <Input id="commissionRate" type="number" placeholder="15" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="accountManager">Account Manager</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Assign manager" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="sarah">Sarah Johnson</SelectItem>
                  <SelectItem value="mike">Mike Chen</SelectItem>
                  <SelectItem value="emily">Emily Rodriguez</SelectItem>
                  <SelectItem value="david">David Park</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="partnerTags">Tags (comma-separated)</Label>
            <Input id="partnerTags" placeholder="new-partner, technology, strategic" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
            <Textarea id="notes" placeholder="Additional notes about the partner" />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsCreatePartnerDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsCreatePartnerDialogOpen(false)}>
            Add Partner
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  const CreateProgramDialog = () => (
    <Dialog open={isCreateProgramDialogOpen} onOpenChange={setIsCreateProgramDialogOpen}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Create Partner Program</DialogTitle>
          <DialogDescription>
            Launch a new program for your partner ecosystem.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-6 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="programName">Program Name</Label>
              <Input id="programName" placeholder="Enter program name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="programType">Program Type</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="certification">Certification</SelectItem>
                  <SelectItem value="training">Training</SelectItem>
                  <SelectItem value="incentive">Incentive</SelectItem>
                  <SelectItem value="marketing">Marketing</SelectItem>
                  <SelectItem value="technical">Technical</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="programDescription">Description</Label>
            <Textarea id="programDescription" placeholder="Describe the program objectives and benefits" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="startDate">Start Date</Label>
              <Input id="startDate" type="date" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="endDate">End Date (Optional)</Label>
              <Input id="endDate" type="date" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="programBudget">Budget ($)</Label>
              <Input id="programBudget" type="number" placeholder="Program budget" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="programManager">Program Manager</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Assign manager" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="sarah">Sarah Johnson</SelectItem>
                  <SelectItem value="mike">Mike Chen</SelectItem>
                  <SelectItem value="emily">Emily Rodriguez</SelectItem>
                  <SelectItem value="david">David Park</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Program Requirements</Label>
            <Textarea placeholder="List program requirements (one per line)" />
          </div>

          <div className="space-y-2">
            <Label>Program Benefits</Label>
            <Textarea placeholder="List program benefits (one per line)" />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsCreateProgramDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsCreateProgramDialogOpen(false)}>
            Create Program
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <Handshake className="h-8 w-8 text-blue-600" />
            Partner Management
          </h1>
          <p className="text-muted-foreground">
            Manage partner relationships and programs
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" onClick={() => setIsCreateProgramDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Program
          </Button>
          <Button onClick={() => setIsCreatePartnerDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Partner
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Partners</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{partnerStats.total}</div>
            <p className="text-xs text-muted-foreground">
              {partnerStats.active} active
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Partner Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${partnerStats.totalRevenue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              This year
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Commissions Paid</CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${partnerStats.totalCommission.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Total earned
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Performance</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{partnerStats.avgPerformance.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Performance score
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Programs Active</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{programs.filter(p => p.status === 'active').length}</div>
            <p className="text-xs text-muted-foreground">
              Running programs
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="partners">Partners</TabsTrigger>
          <TabsTrigger value="programs">Programs</TabsTrigger>
          <TabsTrigger value="onboarding">Onboarding</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="partners" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Partner Directory</CardTitle>
              <CardDescription>
                Manage your partner relationships and performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4 mb-6">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="Search partners..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="inactive">Inactive</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="suspended">Suspended</SelectItem>
                    <SelectItem value="terminated">Terminated</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={filterType} onValueChange={setFilterType}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="reseller">Reseller</SelectItem>
                    <SelectItem value="distributor">Distributor</SelectItem>
                    <SelectItem value="technology">Technology</SelectItem>
                    <SelectItem value="referral">Referral</SelectItem>
                    <SelectItem value="strategic">Strategic</SelectItem>
                    <SelectItem value="channel">Channel</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={filterTier} onValueChange={setFilterTier}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Tier" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Tiers</SelectItem>
                    <SelectItem value="bronze">Bronze</SelectItem>
                    <SelectItem value="silver">Silver</SelectItem>
                    <SelectItem value="gold">Gold</SelectItem>
                    <SelectItem value="platinum">Platinum</SelectItem>
                    <SelectItem value="diamond">Diamond</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Partner</TableHead>
                      <TableHead>Type & Tier</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Performance</TableHead>
                      <TableHead>Revenue</TableHead>
                      <TableHead>Commission</TableHead>
                      <TableHead>Region</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredPartners.map((partner) => (
                      <TableRow key={partner.id}>
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <Avatar className="h-10 w-10">
                              <AvatarImage src={partner.logo} alt={partner.name} />
                              <AvatarFallback>{partner.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                            </Avatar>
                            <div>
                              <div className="font-medium">{partner.name}</div>
                              <div className="text-sm text-muted-foreground">{partner.company}</div>
                              <div className="text-xs text-muted-foreground">{partner.email}</div>
                              <div className="flex items-center gap-1 mt-1">
                                {partner.tags.map((tag, index) => (
                                  <Badge key={index} variant="secondary" className="text-xs">
                                    {tag}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="flex items-center gap-2">
                              {getTypeIcon(partner.type)}
                              <span className="capitalize text-sm">{partner.type.replace('-', ' ')}</span>
                            </div>
                            <Badge className={getTierColor(partner.tier)}>
                              {partner.tier}
                            </Badge>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <Badge className={getStatusColor(partner.status)}>
                              {partner.status}
                            </Badge>
                            <div className="text-xs text-muted-foreground">
                              Onboarding: <Badge className={getOnboardingStatusColor(partner.onboardingStatus)} variant="outline">
                                {partner.onboardingStatus.replace('-', ' ')}
                              </Badge>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">{partner.performanceScore}%</div>
                            <Progress value={partner.performanceScore} className="h-1 w-16" />
                            <div className="text-xs text-muted-foreground">
                              {partner.deals} deals, {partner.leads} leads
                            </div>
                            {partner.satisfactionScore > 0 && (
                              <div className="text-xs text-muted-foreground">
                                ⭐ {partner.satisfactionScore}/5
                              </div>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm font-medium">
                            ${partner.revenue.toLocaleString()}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {partner.deals} deals
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm font-medium">
                            ${partner.totalCommission.toLocaleString()}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {partner.commissionRate}% rate
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">{partner.region}</div>
                          <div className="text-xs text-muted-foreground">{partner.country}</div>
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex items-center justify-end gap-2">
                            <Button variant="ghost" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Mail className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm" className="text-red-600">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="programs" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Partner Programs</CardTitle>
              <CardDescription>
                Manage certification, training, and incentive programs
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Program</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Participants</TableHead>
                      <TableHead>Completion</TableHead>
                      <TableHead>Budget</TableHead>
                      <TableHead>ROI</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {programs.map((program) => (
                      <TableRow key={program.id}>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="font-medium">{program.name}</div>
                            <p className="text-sm text-muted-foreground">{program.description}</p>
                            <div className="text-xs text-muted-foreground">
                              Manager: {program.manager}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="capitalize">
                            {program.type}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge className={getStatusColor(program.status)}>
                            {program.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm font-medium">{program.participants}</div>
                          <div className="text-xs text-muted-foreground">participants</div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">{program.completionRate}%</div>
                            <Progress value={program.completionRate} className="h-1 w-16" />
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">
                              ${program.budget.toLocaleString()}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              ${program.spent.toLocaleString()} spent
                            </div>
                            <Progress 
                              value={(program.spent / program.budget) * 100} 
                              className="h-1 w-16"
                            />
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm font-medium text-green-600">
                            {program.roi}%
                          </div>
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex items-center justify-end gap-2">
                            <Button variant="ghost" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Settings className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="onboarding" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Partner Onboarding</CardTitle>
              <CardDescription>
                Track partner onboarding progress and status
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {partners.filter(p => p.onboardingStatus !== 'completed').map((partner) => (
                  <div key={partner.id} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <Avatar className="h-8 w-8">
                          <AvatarImage src={partner.logo} alt={partner.name} />
                          <AvatarFallback>{partner.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <div>
                          <div className="font-medium">{partner.name}</div>
                          <div className="text-sm text-muted-foreground">{partner.company}</div>
                        </div>
                      </div>
                      <Badge className={getOnboardingStatusColor(partner.onboardingStatus)}>
                        {partner.onboardingStatus.replace('-', ' ')}
                      </Badge>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Onboarding Progress</span>
                        <span>
                          {partner.onboardingStatus === 'in-progress' ? '60%' : 
                           partner.onboardingStatus === 'on-hold' ? '30%' : '0%'}
                        </span>
                      </div>
                      <Progress 
                        value={partner.onboardingStatus === 'in-progress' ? 60 : 
                               partner.onboardingStatus === 'on-hold' ? 30 : 0} 
                        className="h-2"
                      />
                    </div>

                    <div className="flex items-center justify-between mt-4">
                      <div className="text-sm text-muted-foreground">
                        Account Manager: {partner.accountManager}
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm">
                          <MessageSquare className="h-4 w-4 mr-1" />
                          Contact
                        </Button>
                        <Button size="sm">
                          <PlayCircle className="h-4 w-4 mr-1" />
                          Continue
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Partner Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {partners.filter(p => p.performanceScore > 0).map((partner) => (
                    <div key={partner.id} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Avatar className="h-6 w-6">
                          <AvatarImage src={partner.logo} alt={partner.name} />
                          <AvatarFallback className="text-xs">{partner.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <span className="text-sm">{partner.company}</span>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{partner.performanceScore}%</div>
                        <div className="text-xs text-muted-foreground">${partner.revenue.toLocaleString()}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Program ROI</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {programs.map((program) => (
                    <div key={program.id} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>{program.name}</span>
                        <span className="text-green-600">{program.roi}%</span>
                      </div>
                      <Progress value={Math.min(program.roi, 100)} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      <CreatePartnerDialog />
      <CreateProgramDialog />
    </div>
  );
}