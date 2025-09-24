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
import { 
  PenTool, Plus, Filter, Search, Eye, Edit, Trash2, Upload, Download, 
  Calendar, Clock, User, Tag, Globe, FileText, Image, Video, 
  BarChart3, TrendingUp, Share2, Copy, Archive, Star, CheckCircle,
  AlertCircle, XCircle, PlayCircle, PauseCircle, RefreshCw
} from 'lucide-react';

interface ContentItem {
  id: number;
  title: string;
  type: 'blog' | 'social' | 'email' | 'landing' | 'video' | 'infographic';
  status: 'draft' | 'review' | 'approved' | 'published' | 'archived';
  author: string;
  createdDate: string;
  publishDate?: string;
  lastModified: string;
  views: number;
  engagement: number;
  tags: string[];
  category: string;
  wordCount?: number;
  readTime?: string;
  thumbnail?: string;
  description: string;
}

export function ContentPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedContent, setSelectedContent] = useState<ContentItem | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('list');

  const contentItems: ContentItem[] = [
    {
      id: 1,
      title: 'Complete Guide to Digital Marketing in 2024',
      type: 'blog',
      status: 'published',
      author: 'Sarah Johnson',
      createdDate: '2024-01-15',
      publishDate: '2024-01-20',
      lastModified: '2024-01-18',
      views: 15420,
      engagement: 8.5,
      tags: ['digital marketing', 'strategy', '2024 trends'],
      category: 'Education',
      wordCount: 2850,
      readTime: '12 min',
      description: 'Comprehensive guide covering the latest digital marketing strategies and trends for 2024.'
    },
    {
      id: 2,
      title: 'Product Launch Social Media Campaign',
      type: 'social',
      status: 'approved',
      author: 'Mike Chen',
      createdDate: '2024-01-22',
      publishDate: '2024-02-01',
      lastModified: '2024-01-25',
      views: 0,
      engagement: 0,
      tags: ['product launch', 'social media', 'campaign'],
      category: 'Campaigns',
      description: 'Multi-platform social media content for upcoming product launch.'
    },
    {
      id: 3,
      title: 'Welcome Email Series Template',
      type: 'email',
      status: 'draft',
      author: 'Emily Rodriguez',
      createdDate: '2024-01-28',
      lastModified: '2024-01-30',
      views: 0,
      engagement: 0,
      tags: ['email', 'welcome series', 'automation'],
      category: 'Email Marketing',
      description: 'Automated welcome email series for new subscribers.'
    },
    {
      id: 4,
      title: 'Customer Success Stories Landing Page',
      type: 'landing',
      status: 'review',
      author: 'David Park',
      createdDate: '2024-01-20',
      lastModified: '2024-01-29',
      views: 2340,
      engagement: 12.3,
      tags: ['landing page', 'testimonials', 'conversion'],
      category: 'Website',
      description: 'Dedicated landing page showcasing customer success stories and testimonials.'
    },
    {
      id: 5,
      title: 'Product Demo Video',
      type: 'video',
      status: 'published',
      author: 'Lisa Wang',
      createdDate: '2024-01-10',
      publishDate: '2024-01-15',
      lastModified: '2024-01-12',
      views: 8920,
      engagement: 15.7,
      tags: ['video', 'product demo', 'tutorial'],
      category: 'Video Content',
      description: 'Comprehensive product demonstration video for new users.'
    },
    {
      id: 6,
      title: 'Industry Statistics Infographic',
      type: 'infographic',
      status: 'archived',
      author: 'Tom Wilson',
      createdDate: '2023-12-15',
      publishDate: '2023-12-20',
      lastModified: '2023-12-18',
      views: 5680,
      engagement: 9.2,
      tags: ['infographic', 'statistics', 'industry'],
      category: 'Visual Content',
      description: 'Visual representation of key industry statistics and trends.'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800';
      case 'approved': return 'bg-blue-100 text-blue-800';
      case 'review': return 'bg-yellow-100 text-yellow-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      case 'archived': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'blog': return FileText;
      case 'social': return Share2;
      case 'email': return FileText;
      case 'landing': return Globe;
      case 'video': return Video;
      case 'infographic': return Image;
      default: return FileText;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'published': return CheckCircle;
      case 'approved': return CheckCircle;
      case 'review': return AlertCircle;
      case 'draft': return Edit;
      case 'archived': return Archive;
      default: return Edit;
    }
  };

  const filteredContent = contentItems.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesType = filterType === 'all' || item.type === filterType;
    const matchesStatus = filterStatus === 'all' || item.status === filterStatus;
    return matchesSearch && matchesType && matchesStatus;
  });

  const contentStats = {
    total: contentItems.length,
    published: contentItems.filter(item => item.status === 'published').length,
    draft: contentItems.filter(item => item.status === 'draft').length,
    review: contentItems.filter(item => item.status === 'review').length,
    totalViews: contentItems.reduce((sum, item) => sum + item.views, 0),
    avgEngagement: contentItems.reduce((sum, item) => sum + item.engagement, 0) / contentItems.length
  };

  const CreateContentDialog = () => (
    <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create New Content</DialogTitle>
          <DialogDescription>
            Create a new piece of content for your marketing campaigns.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="title">Title</Label>
              <Input id="title" placeholder="Enter content title" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="type">Content Type</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="blog">Blog Post</SelectItem>
                  <SelectItem value="social">Social Media</SelectItem>
                  <SelectItem value="email">Email</SelectItem>
                  <SelectItem value="landing">Landing Page</SelectItem>
                  <SelectItem value="video">Video</SelectItem>
                  <SelectItem value="infographic">Infographic</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="category">Category</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="education">Education</SelectItem>
                  <SelectItem value="campaigns">Campaigns</SelectItem>
                  <SelectItem value="email-marketing">Email Marketing</SelectItem>
                  <SelectItem value="website">Website</SelectItem>
                  <SelectItem value="video-content">Video Content</SelectItem>
                  <SelectItem value="visual-content">Visual Content</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="author">Author</Label>
              <Input id="author" placeholder="Content author" />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea id="description" placeholder="Brief description of the content" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="tags">Tags (comma-separated)</Label>
            <Input id="tags" placeholder="tag1, tag2, tag3" />
          </div>
          <div className="flex items-center space-x-2">
            <Switch id="schedule" />
            <Label htmlFor="schedule">Schedule for later</Label>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(false)}>
            Create Content
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
            <PenTool className="h-8 w-8 text-blue-600" />
            Content Management
          </h1>
          <p className="text-muted-foreground">
            Create, manage, and publish marketing content across all channels
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Upload className="h-4 w-4 mr-2" />
            Import
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Create Content
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Content</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{contentStats.total}</div>
            <p className="text-xs text-muted-foreground">
              {contentStats.published} published
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{contentStats.totalViews.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Across all content
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Engagement</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{contentStats.avgEngagement.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Engagement rate
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">In Review</CardTitle>
            <AlertCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{contentStats.review}</div>
            <p className="text-xs text-muted-foreground">
              Awaiting approval
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Content Library</CardTitle>
            <div className="flex items-center gap-2">
              <Button
                variant={viewMode === 'list' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('list')}
              >
                List
              </Button>
              <Button
                variant={viewMode === 'grid' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('grid')}
              >
                Grid
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search content..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Content Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="blog">Blog Posts</SelectItem>
                <SelectItem value="social">Social Media</SelectItem>
                <SelectItem value="email">Email</SelectItem>
                <SelectItem value="landing">Landing Pages</SelectItem>
                <SelectItem value="video">Video</SelectItem>
                <SelectItem value="infographic">Infographics</SelectItem>
              </SelectContent>
            </Select>
            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="draft">Draft</SelectItem>
                <SelectItem value="review">In Review</SelectItem>
                <SelectItem value="approved">Approved</SelectItem>
                <SelectItem value="published">Published</SelectItem>
                <SelectItem value="archived">Archived</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Content Table */}
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Content</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Author</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Views</TableHead>
                  <TableHead>Engagement</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredContent.map((item) => {
                  const TypeIcon = getTypeIcon(item.type);
                  const StatusIcon = getStatusIcon(item.status);
                  
                  return (
                    <TableRow key={item.id}>
                      <TableCell>
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <TypeIcon className="h-4 w-4 text-muted-foreground" />
                            <span className="font-medium">{item.title}</span>
                          </div>
                          <p className="text-sm text-muted-foreground">{item.description}</p>
                          <div className="flex items-center gap-1">
                            {item.tags.map((tag, index) => (
                              <Badge key={index} variant="secondary" className="text-xs">
                                {tag}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className="capitalize">
                          {item.type}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <StatusIcon className="h-4 w-4" />
                          <Badge className={getStatusColor(item.status)}>
                            {item.status}
                          </Badge>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <User className="h-4 w-4 text-muted-foreground" />
                          {item.author}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          <div className="flex items-center gap-1 text-sm">
                            <Calendar className="h-3 w-3" />
                            {item.createdDate}
                          </div>
                          {item.publishDate && (
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              <Globe className="h-3 w-3" />
                              Published: {item.publishDate}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1">
                          <Eye className="h-4 w-4 text-muted-foreground" />
                          {item.views.toLocaleString()}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1">
                          <TrendingUp className="h-4 w-4 text-muted-foreground" />
                          {item.engagement}%
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
                            <Copy className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-red-600">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      <CreateContentDialog />
    </div>
  );
}