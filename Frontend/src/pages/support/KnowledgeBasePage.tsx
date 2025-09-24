import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Plus, Search, Filter, BookOpen, FileText, Video, HelpCircle, Eye, ThumbsUp, Clock, Edit } from 'lucide-react';
import { useState } from 'react';

export function KnowledgeBasePage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const articles = [
    {
      id: 1,
      title: 'Getting Started with Your Account',
      category: 'Getting Started',
      type: 'Article',
      status: 'Published',
      author: 'Sarah Johnson',
      lastUpdated: '2024-01-15',
      views: 1250,
      likes: 45,
      helpful: 89,
      tags: ['setup', 'account', 'basics']
    },
    {
      id: 2,
      title: 'How to Set Up Two-Factor Authentication',
      category: 'Security',
      type: 'Article',
      status: 'Published',
      author: 'Mike Chen',
      lastUpdated: '2024-01-14',
      views: 890,
      likes: 32,
      helpful: 78,
      tags: ['security', '2fa', 'account']
    },
    {
      id: 3,
      title: 'Product Demo Video: Advanced Features',
      category: 'Tutorials',
      type: 'Video',
      status: 'Published',
      author: 'Emily Davis',
      lastUpdated: '2024-01-12',
      views: 2100,
      likes: 87,
      helpful: 94,
      tags: ['video', 'features', 'advanced']
    },
    {
      id: 4,
      title: 'Troubleshooting Common Login Issues',
      category: 'Troubleshooting',
      type: 'Article',
      status: 'Draft',
      author: 'John Smith',
      lastUpdated: '2024-01-10',
      views: 0,
      likes: 0,
      helpful: 0,
      tags: ['login', 'troubleshooting', 'issues']
    },
    {
      id: 5,
      title: 'API Integration Guide',
      category: 'Developer',
      type: 'Guide',
      status: 'Published',
      author: 'David Wilson',
      lastUpdated: '2024-01-08',
      views: 1450,
      likes: 67,
      helpful: 85,
      tags: ['api', 'integration', 'developer']
    }
  ];

  const categories = [
    { name: 'Getting Started', count: 12, icon: BookOpen },
    { name: 'Security', count: 8, icon: HelpCircle },
    { name: 'Tutorials', count: 15, icon: Video },
    { name: 'Troubleshooting', count: 23, icon: FileText },
    { name: 'Developer', count: 9, icon: FileText },
    { name: 'Billing', count: 7, icon: FileText },
  ];

  const recentActivity = [
    {
      action: 'Article viewed',
      article: 'Getting Started with Your Account',
      user: 'Anonymous',
      timestamp: '2 minutes ago'
    },
    {
      action: 'Article liked',
      article: 'API Integration Guide',
      user: 'developer@company.com',
      timestamp: '5 minutes ago'
    },
    {
      action: 'Article updated',
      article: 'How to Set Up Two-Factor Authentication',
      user: 'Mike Chen',
      timestamp: '1 hour ago'
    },
    {
      action: 'New article created',
      article: 'Advanced Reporting Features',
      user: 'Sarah Johnson',
      timestamp: '3 hours ago'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Published': return 'default';
      case 'Draft': return 'secondary';
      case 'Review': return 'outline';
      default: return 'outline';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'Article': return <FileText className="h-4 w-4" />;
      case 'Video': return <Video className="h-4 w-4" />;
      case 'Guide': return <BookOpen className="h-4 w-4" />;
      default: return <FileText className="h-4 w-4" />;
    }
  };

  const filteredArticles = articles.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         article.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || article.category === selectedCategory;
    const matchesStatus = selectedStatus === 'all' || article.status === selectedStatus;
    
    return matchesSearch && matchesCategory && matchesStatus;
  });

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Knowledge Base</h1>
          <p className="text-muted-foreground">
            Manage help articles and documentation
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Filter className="mr-2 h-4 w-4" />
            Analytics
          </Button>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                New Article
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Create New Article</DialogTitle>
                <DialogDescription>
                  Add a new help article to your knowledge base
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="title" className="text-right">Title</Label>
                  <Input id="title" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="category" className="text-right">Category</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="getting-started">Getting Started</SelectItem>
                      <SelectItem value="security">Security</SelectItem>
                      <SelectItem value="tutorials">Tutorials</SelectItem>
                      <SelectItem value="troubleshooting">Troubleshooting</SelectItem>
                      <SelectItem value="developer">Developer</SelectItem>
                      <SelectItem value="billing">Billing</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="type" className="text-right">Type</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="article">Article</SelectItem>
                      <SelectItem value="video">Video</SelectItem>
                      <SelectItem value="guide">Guide</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="tags" className="text-right">Tags</Label>
                  <Input id="tags" placeholder="Comma separated tags" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="content" className="text-right">Content</Label>
                  <Textarea id="content" className="col-span-3 min-h-[100px]" />
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Save as Draft
                </Button>
                <Button onClick={() => setIsCreateDialogOpen(false)}>
                  Publish
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Knowledge Base Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Articles</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{articles.length}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+3</span> this week
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {articles.reduce((sum, article) => sum + article.views, 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+12%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Helpfulness</CardTitle>
            <ThumbsUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(articles.reduce((sum, article) => sum + article.helpful, 0) / articles.length)}%
            </div>
            <p className="text-xs text-muted-foreground">
              User satisfaction rate
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Published</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {articles.filter(article => article.status === 'Published').length}
            </div>
            <p className="text-xs text-muted-foreground">
              {articles.filter(article => article.status === 'Draft').length} in draft
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="articles" className="space-y-4">
        <TabsList>
          <TabsTrigger value="articles">Articles</TabsTrigger>
          <TabsTrigger value="categories">Categories</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
        </TabsList>

        <TabsContent value="articles" className="space-y-4">
          {/* Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <Input
                      placeholder="Search articles..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    <SelectItem value="Getting Started">Getting Started</SelectItem>
                    <SelectItem value="Security">Security</SelectItem>
                    <SelectItem value="Tutorials">Tutorials</SelectItem>
                    <SelectItem value="Troubleshooting">Troubleshooting</SelectItem>
                    <SelectItem value="Developer">Developer</SelectItem>
                    <SelectItem value="Billing">Billing</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="Published">Published</SelectItem>
                    <SelectItem value="Draft">Draft</SelectItem>
                    <SelectItem value="Review">Review</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Articles Table */}
          <Card>
            <CardHeader>
              <CardTitle>Knowledge Base Articles</CardTitle>
              <CardDescription>
                {filteredArticles.length} articles found
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Article</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Performance</TableHead>
                    <TableHead>Last Updated</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredArticles.map((article) => (
                    <TableRow key={article.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{article.title}</div>
                          <div className="text-sm text-muted-foreground">
                            by {article.author}
                          </div>
                          <div className="flex gap-1 mt-1">
                            {article.tags.map((tag, index) => (
                              <Badge key={index} variant="outline" className="text-xs">
                                {tag}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>{article.category}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getTypeIcon(article.type)}
                          {article.type}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusColor(article.status)}>
                          {article.status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          <div className="flex items-center gap-2 text-sm">
                            <Eye className="h-3 w-3" />
                            {article.views} views
                          </div>
                          <div className="flex items-center gap-2 text-sm">
                            <ThumbsUp className="h-3 w-3" />
                            {article.helpful}% helpful
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>{article.lastUpdated}</TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="outline" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            View
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="categories" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Knowledge Base Categories</CardTitle>
              <CardDescription>
                Organize your articles by categories
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {categories.map((category, index) => {
                  const IconComponent = category.icon;
                  return (
                    <Card key={index} className="hover:shadow-md transition-shadow cursor-pointer">
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <CardTitle className="text-base flex items-center gap-2">
                            <IconComponent className="h-4 w-4" />
                            {category.name}
                          </CardTitle>
                          <Badge variant="secondary">{category.count}</Badge>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm" className="flex-1">
                            Manage
                          </Button>
                          <Button size="sm" className="flex-1">
                            View Articles
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="activity" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Latest activity in your knowledge base
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <Clock className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <div className="font-medium">{activity.action}</div>
                        <div className="text-sm text-muted-foreground">
                          "{activity.article}" by {activity.user}
                        </div>
                      </div>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {activity.timestamp}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}