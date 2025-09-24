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
import { 
  Calendar, Plus, Filter, Search, Eye, Edit, Trash2, Users, 
  Clock, User, Tag, Globe, FileText, BarChart3, 
  TrendingUp, Share2, Copy, Archive, Star, CheckCircle,
  AlertCircle, XCircle, PlayCircle, PauseCircle, RefreshCw,
  Zap, Settings, Download, Upload, PieChart, Activity,
  MapPin, DollarSign, ShoppingCart, Mail, Phone, Smartphone,
  Video, Mic, Camera, Monitor, Headphones, MessageSquare,
  ExternalLink, QrCode, Ticket, Gift, Award, Target,
  Megaphone, Radio, Tv, Newspaper, BookOpen, Coffee
} from 'lucide-react';

interface Event {
  id: number;
  name: string;
  description: string;
  type: 'webinar' | 'conference' | 'workshop' | 'product-launch' | 'networking' | 'trade-show';
  status: 'draft' | 'scheduled' | 'live' | 'completed' | 'cancelled';
  startDate: string;
  endDate: string;
  location: string;
  isVirtual: boolean;
  maxAttendees: number;
  registeredAttendees: number;
  actualAttendees?: number;
  registrationFee: number;
  revenue: number;
  organizer: string;
  tags: string[];
  campaignId?: number;
  conversionRate: number;
  engagementScore: number;
  satisfaction: number;
}

interface Campaign {
  id: number;
  name: string;
  description: string;
  type: 'email' | 'social' | 'display' | 'search' | 'content' | 'event' | 'influencer';
  status: 'draft' | 'active' | 'paused' | 'completed' | 'cancelled';
  startDate: string;
  endDate?: string;
  budget: number;
  spent: number;
  reach: number;
  impressions: number;
  clicks: number;
  conversions: number;
  leads: number;
  revenue: number;
  targetAudience: string[];
  channels: string[];
  manager: string;
  tags: string[];
  events: number[];
}

export function EventsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [isCreateEventDialogOpen, setIsCreateEventDialogOpen] = useState(false);
  const [isCreateCampaignDialogOpen, setIsCreateCampaignDialogOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('events');

  const events: Event[] = [
    {
      id: 1,
      name: 'Product Launch Webinar',
      description: 'Introducing our latest product features and capabilities',
      type: 'webinar',
      status: 'scheduled',
      startDate: '2024-02-15T14:00:00',
      endDate: '2024-02-15T15:30:00',
      location: 'Virtual - Zoom',
      isVirtual: true,
      maxAttendees: 500,
      registeredAttendees: 342,
      registrationFee: 0,
      revenue: 0,
      organizer: 'Sarah Johnson',
      tags: ['product-launch', 'webinar', 'virtual'],
      campaignId: 1,
      conversionRate: 0,
      engagementScore: 0,
      satisfaction: 0
    },
    {
      id: 2,
      name: 'Industry Conference 2024',
      description: 'Annual industry conference with keynote speakers and networking',
      type: 'conference',
      status: 'completed',
      startDate: '2024-01-20T09:00:00',
      endDate: '2024-01-22T17:00:00',
      location: 'San Francisco Convention Center',
      isVirtual: false,
      maxAttendees: 1000,
      registeredAttendees: 856,
      actualAttendees: 742,
      registrationFee: 299,
      revenue: 255844,
      organizer: 'Mike Chen',
      tags: ['conference', 'networking', 'industry'],
      campaignId: 2,
      conversionRate: 18.5,
      engagementScore: 87,
      satisfaction: 4.6
    },
    {
      id: 3,
      name: 'Customer Success Workshop',
      description: 'Hands-on workshop for maximizing customer success strategies',
      type: 'workshop',
      status: 'live',
      startDate: '2024-02-01T10:00:00',
      endDate: '2024-02-01T16:00:00',
      location: 'Virtual - Microsoft Teams',
      isVirtual: true,
      maxAttendees: 50,
      registeredAttendees: 48,
      actualAttendees: 45,
      registrationFee: 149,
      revenue: 7152,
      organizer: 'Emily Rodriguez',
      tags: ['workshop', 'customer-success', 'training'],
      conversionRate: 22.2,
      engagementScore: 92,
      satisfaction: 4.8
    },
    {
      id: 4,
      name: 'Tech Trade Show Booth',
      description: 'Showcase our solutions at the major tech trade show',
      type: 'trade-show',
      status: 'scheduled',
      startDate: '2024-03-10T09:00:00',
      endDate: '2024-03-12T18:00:00',
      location: 'Las Vegas Convention Center',
      isVirtual: false,
      maxAttendees: 0,
      registeredAttendees: 0,
      registrationFee: 0,
      revenue: 0,
      organizer: 'David Park',
      tags: ['trade-show', 'booth', 'b2b'],
      campaignId: 3,
      conversionRate: 0,
      engagementScore: 0,
      satisfaction: 0
    },
    {
      id: 5,
      name: 'Networking Mixer',
      description: 'Casual networking event for industry professionals',
      type: 'networking',
      status: 'draft',
      startDate: '2024-02-28T18:00:00',
      endDate: '2024-02-28T21:00:00',
      location: 'Downtown Hotel Rooftop',
      isVirtual: false,
      maxAttendees: 100,
      registeredAttendees: 0,
      registrationFee: 25,
      revenue: 0,
      organizer: 'Lisa Wang',
      tags: ['networking', 'mixer', 'social'],
      conversionRate: 0,
      engagementScore: 0,
      satisfaction: 0
    }
  ];

  const campaigns: Campaign[] = [
    {
      id: 1,
      name: 'Q1 Product Launch Campaign',
      description: 'Comprehensive campaign for new product launch',
      type: 'content',
      status: 'active',
      startDate: '2024-01-15',
      endDate: '2024-03-31',
      budget: 50000,
      spent: 32500,
      reach: 125000,
      impressions: 450000,
      clicks: 12500,
      conversions: 856,
      leads: 1200,
      revenue: 185000,
      targetAudience: ['enterprise', 'mid-market', 'tech-savvy'],
      channels: ['email', 'social', 'webinar', 'content'],
      manager: 'Sarah Johnson',
      tags: ['product-launch', 'q1', 'multi-channel'],
      events: [1]
    },
    {
      id: 2,
      name: 'Industry Leadership Campaign',
      description: 'Establish thought leadership in the industry',
      type: 'event',
      status: 'completed',
      startDate: '2024-01-01',
      endDate: '2024-01-31',
      budget: 75000,
      spent: 68500,
      reach: 85000,
      impressions: 320000,
      clicks: 8500,
      conversions: 742,
      leads: 980,
      revenue: 255844,
      targetAudience: ['c-level', 'decision-makers', 'industry-leaders'],
      channels: ['conference', 'speaking', 'networking'],
      manager: 'Mike Chen',
      tags: ['thought-leadership', 'conference', 'networking'],
      events: [2]
    },
    {
      id: 3,
      name: 'Trade Show Presence',
      description: 'Maximize visibility at major industry trade shows',
      type: 'event',
      status: 'scheduled',
      startDate: '2024-03-01',
      endDate: '2024-03-31',
      budget: 100000,
      spent: 15000,
      reach: 0,
      impressions: 0,
      clicks: 0,
      conversions: 0,
      leads: 0,
      revenue: 0,
      targetAudience: ['enterprise', 'partners', 'prospects'],
      channels: ['trade-show', 'booth', 'demos'],
      manager: 'David Park',
      tags: ['trade-show', 'b2b', 'demos'],
      events: [4]
    }
  ];

  const getEventStatusColor = (status: string) => {
    switch (status) {
      case 'scheduled': return 'bg-blue-100 text-blue-800';
      case 'live': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-gray-100 text-gray-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCampaignStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'webinar': return <Video className="h-4 w-4" />;
      case 'conference': return <Users className="h-4 w-4" />;
      case 'workshop': return <BookOpen className="h-4 w-4" />;
      case 'product-launch': return <Megaphone className="h-4 w-4" />;
      case 'networking': return <Coffee className="h-4 w-4" />;
      case 'trade-show': return <Monitor className="h-4 w-4" />;
      default: return <Calendar className="h-4 w-4" />;
    }
  };

  const filteredEvents = events.filter(event => {
    const matchesSearch = event.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         event.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         event.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = filterStatus === 'all' || event.status === filterStatus;
    const matchesType = filterType === 'all' || event.type === filterType;
    return matchesSearch && matchesStatus && matchesType;
  });

  const eventStats = {
    total: events.length,
    scheduled: events.filter(e => e.status === 'scheduled').length,
    totalAttendees: events.reduce((sum, e) => sum + e.registeredAttendees, 0),
    totalRevenue: events.reduce((sum, e) => sum + e.revenue, 0)
  };

  const campaignStats = {
    total: campaigns.length,
    active: campaigns.filter(c => c.status === 'active').length,
    totalBudget: campaigns.reduce((sum, c) => sum + c.budget, 0),
    totalSpent: campaigns.reduce((sum, c) => sum + c.spent, 0),
    totalRevenue: campaigns.reduce((sum, c) => sum + c.revenue, 0)
  };

  const CreateEventDialog = () => (
    <Dialog open={isCreateEventDialogOpen} onOpenChange={setIsCreateEventDialogOpen}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Create New Event</DialogTitle>
          <DialogDescription>
            Plan and organize a new marketing event or activity.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-6 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="eventName">Event Name</Label>
              <Input id="eventName" placeholder="Enter event name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="eventType">Event Type</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="webinar">Webinar</SelectItem>
                  <SelectItem value="conference">Conference</SelectItem>
                  <SelectItem value="workshop">Workshop</SelectItem>
                  <SelectItem value="product-launch">Product Launch</SelectItem>
                  <SelectItem value="networking">Networking</SelectItem>
                  <SelectItem value="trade-show">Trade Show</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="eventDescription">Description</Label>
            <Textarea id="eventDescription" placeholder="Describe the event" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="startDate">Start Date & Time</Label>
              <Input id="startDate" type="datetime-local" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="endDate">End Date & Time</Label>
              <Input id="endDate" type="datetime-local" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>
              <Input id="location" placeholder="Event location or platform" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxAttendees">Max Attendees</Label>
              <Input id="maxAttendees" type="number" placeholder="Maximum capacity" />
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Switch id="isVirtual" />
            <Label htmlFor="isVirtual">Virtual Event</Label>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="registrationFee">Registration Fee ($)</Label>
              <Input id="registrationFee" type="number" placeholder="0" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="organizer">Organizer</Label>
              <Input id="organizer" placeholder="Event organizer" />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="eventTags">Tags (comma-separated)</Label>
            <Input id="eventTags" placeholder="tag1, tag2, tag3" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="linkedCampaign">Link to Campaign (Optional)</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select campaign" />
              </SelectTrigger>
              <SelectContent>
                {campaigns.map((campaign) => (
                  <SelectItem key={campaign.id} value={campaign.id.toString()}>
                    {campaign.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsCreateEventDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsCreateEventDialogOpen(false)}>
            Create Event
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  const CreateCampaignDialog = () => (
    <Dialog open={isCreateCampaignDialogOpen} onOpenChange={setIsCreateCampaignDialogOpen}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Create New Campaign</DialogTitle>
          <DialogDescription>
            Launch a new marketing campaign with events and activities.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-6 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="campaignName">Campaign Name</Label>
              <Input id="campaignName" placeholder="Enter campaign name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="campaignType">Campaign Type</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="email">Email Marketing</SelectItem>
                  <SelectItem value="social">Social Media</SelectItem>
                  <SelectItem value="display">Display Advertising</SelectItem>
                  <SelectItem value="search">Search Marketing</SelectItem>
                  <SelectItem value="content">Content Marketing</SelectItem>
                  <SelectItem value="event">Event Marketing</SelectItem>
                  <SelectItem value="influencer">Influencer Marketing</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="campaignDescription">Description</Label>
            <Textarea id="campaignDescription" placeholder="Describe the campaign objectives" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="campaignStartDate">Start Date</Label>
              <Input id="campaignStartDate" type="date" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="campaignEndDate">End Date (Optional)</Label>
              <Input id="campaignEndDate" type="date" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="budget">Budget ($)</Label>
              <Input id="budget" type="number" placeholder="Campaign budget" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="manager">Campaign Manager</Label>
              <Input id="manager" placeholder="Manager name" />
            </div>
          </div>

          <div className="space-y-2">
            <Label>Target Audience</Label>
            <div className="grid grid-cols-3 gap-2">
              {['Enterprise', 'Mid-Market', 'Small Business', 'C-Level', 'Decision Makers', 'Tech-Savvy', 'Budget-Conscious', 'Early Adopters', 'Industry Leaders'].map((audience) => (
                <div key={audience} className="flex items-center space-x-2">
                  <Checkbox id={audience} />
                  <Label htmlFor={audience} className="text-sm">{audience}</Label>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Marketing Channels</Label>
            <div className="grid grid-cols-3 gap-2">
              {['Email', 'Social Media', 'Content', 'Events', 'Webinars', 'Trade Shows', 'Display Ads', 'Search Ads', 'Influencer'].map((channel) => (
                <div key={channel} className="flex items-center space-x-2">
                  <Checkbox id={channel} />
                  <Label htmlFor={channel} className="text-sm">{channel}</Label>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="campaignTags">Tags (comma-separated)</Label>
            <Input id="campaignTags" placeholder="tag1, tag2, tag3" />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsCreateCampaignDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsCreateCampaignDialogOpen(false)}>
            Create Campaign
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
            <Calendar className="h-8 w-8 text-purple-600" />
            Events & Campaigns
          </h1>
          <p className="text-muted-foreground">
            Manage marketing events and campaign activities
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" onClick={() => setIsCreateCampaignDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Campaign
          </Button>
          <Button onClick={() => setIsCreateEventDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Event
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Events</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{eventStats.total}</div>
            <p className="text-xs text-muted-foreground">
              {eventStats.scheduled} scheduled
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Attendees</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{eventStats.totalAttendees.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Registered across events
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Event Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${eventStats.totalRevenue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              From registrations
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Campaign ROI</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {campaignStats.totalSpent > 0 ? 
                `${((campaignStats.totalRevenue / campaignStats.totalSpent - 1) * 100).toFixed(1)}%` : 
                '0%'
              }
            </div>
            <p className="text-xs text-muted-foreground">
              Return on investment
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="events">Events</TabsTrigger>
          <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
          <TabsTrigger value="calendar">Calendar</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="events" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Marketing Events</CardTitle>
              <CardDescription>
                Manage your marketing events and activities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4 mb-6">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="Search events..."
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
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="scheduled">Scheduled</SelectItem>
                    <SelectItem value="live">Live</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                    <SelectItem value="cancelled">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={filterType} onValueChange={setFilterType}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="webinar">Webinar</SelectItem>
                    <SelectItem value="conference">Conference</SelectItem>
                    <SelectItem value="workshop">Workshop</SelectItem>
                    <SelectItem value="product-launch">Product Launch</SelectItem>
                    <SelectItem value="networking">Networking</SelectItem>
                    <SelectItem value="trade-show">Trade Show</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Event</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Date & Time</TableHead>
                      <TableHead>Attendees</TableHead>
                      <TableHead>Revenue</TableHead>
                      <TableHead>Performance</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredEvents.map((event) => (
                      <TableRow key={event.id}>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="font-medium">{event.name}</div>
                            <p className="text-sm text-muted-foreground">{event.description}</p>
                            <div className="flex items-center gap-1">
                              {event.tags.map((tag, index) => (
                                <Badge key={index} variant="secondary" className="text-xs">
                                  {tag}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            {getEventTypeIcon(event.type)}
                            <span className="capitalize">{event.type.replace('-', ' ')}</span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge className={getEventStatusColor(event.status)}>
                            {event.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">
                              {new Date(event.startDate).toLocaleDateString()}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {new Date(event.startDate).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - 
                              {new Date(event.endDate).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {event.isVirtual ? '🌐 Virtual' : '📍 ' + event.location}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">
                              {event.registeredAttendees} / {event.maxAttendees || '∞'}
                            </div>
                            {event.actualAttendees && (
                              <div className="text-xs text-muted-foreground">
                                {event.actualAttendees} attended
                              </div>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm font-medium">
                            ${event.revenue.toLocaleString()}
                          </div>
                          {event.registrationFee > 0 && (
                            <div className="text-xs text-muted-foreground">
                              ${event.registrationFee} per ticket
                            </div>
                          )}
                        </TableCell>
                        <TableCell>
                          {event.status === 'completed' && (
                            <div className="space-y-1">
                              <div className="text-xs">
                                <span className="text-muted-foreground">Conv:</span> {event.conversionRate}%
                              </div>
                              <div className="text-xs">
                                <span className="text-muted-foreground">Eng:</span> {event.engagementScore}%
                              </div>
                              <div className="text-xs">
                                <span className="text-muted-foreground">Sat:</span> {event.satisfaction}/5
                              </div>
                            </div>
                          )}
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
                              <Copy className="h-4 w-4" />
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

        <TabsContent value="campaigns" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Marketing Campaigns</CardTitle>
              <CardDescription>
                Track and manage your marketing campaigns
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Campaign</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Budget</TableHead>
                      <TableHead>Performance</TableHead>
                      <TableHead>ROI</TableHead>
                      <TableHead>Events</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {campaigns.map((campaign) => (
                      <TableRow key={campaign.id}>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="font-medium">{campaign.name}</div>
                            <p className="text-sm text-muted-foreground">{campaign.description}</p>
                            <div className="flex items-center gap-1">
                              {campaign.tags.map((tag, index) => (
                                <Badge key={index} variant="secondary" className="text-xs">
                                  {tag}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="capitalize">
                            {campaign.type.replace('-', ' ')}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge className={getCampaignStatusColor(campaign.status)}>
                            {campaign.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">
                              ${campaign.budget.toLocaleString()}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              ${campaign.spent.toLocaleString()} spent
                            </div>
                            <Progress 
                              value={(campaign.spent / campaign.budget) * 100} 
                              className="h-1 w-16"
                            />
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-xs">
                              <span className="text-muted-foreground">Reach:</span> {campaign.reach.toLocaleString()}
                            </div>
                            <div className="text-xs">
                              <span className="text-muted-foreground">Clicks:</span> {campaign.clicks.toLocaleString()}
                            </div>
                            <div className="text-xs">
                              <span className="text-muted-foreground">Conv:</span> {campaign.conversions.toLocaleString()}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm font-medium">
                            {campaign.spent > 0 ? 
                              `${((campaign.revenue / campaign.spent - 1) * 100).toFixed(1)}%` : 
                              '0%'
                            }
                          </div>
                          <div className="text-xs text-muted-foreground">
                            ${campaign.revenue.toLocaleString()} revenue
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">
                            {campaign.events.length} events
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
                            {campaign.status === 'active' ? (
                              <Button variant="ghost" size="sm">
                                <PauseCircle className="h-4 w-4" />
                              </Button>
                            ) : (
                              <Button variant="ghost" size="sm">
                                <PlayCircle className="h-4 w-4" />
                              </Button>
                            )}
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

        <TabsContent value="calendar" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Event Calendar</CardTitle>
              <CardDescription>
                View upcoming events in calendar format
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <Calendar className="h-12 w-12 mx-auto mb-4" />
                <p>Calendar view will be implemented here</p>
                <p className="text-sm">Integration with calendar libraries coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Event Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {events.filter(e => e.status === 'completed').map((event) => (
                    <div key={event.id} className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">{event.name}</div>
                        <div className="text-sm text-muted-foreground">
                          {event.actualAttendees} attendees
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">{event.conversionRate}%</div>
                        <div className="text-sm text-muted-foreground">conversion</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Campaign ROI</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {campaigns.map((campaign) => (
                    <div key={campaign.id} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>{campaign.name}</span>
                        <span>
                          {campaign.spent > 0 ? 
                            `${((campaign.revenue / campaign.spent - 1) * 100).toFixed(1)}%` : 
                            '0%'
                          }
                        </span>
                      </div>
                      <Progress 
                        value={campaign.spent > 0 ? Math.min(((campaign.revenue / campaign.spent - 1) * 100), 100) : 0} 
                        className="h-2"
                      />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      <CreateEventDialog />
      <CreateCampaignDialog />
    </div>
  );
}