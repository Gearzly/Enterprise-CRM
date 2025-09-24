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
import { Progress } from '../../components/ui/progress';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { Plus, Search, Filter, Star, MessageSquare, TrendingUp, TrendingDown, Users, Heart, FileText, BarChart3 } from 'lucide-react';
import { useState } from 'react';

export function FeedbackPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRating, setSelectedRating] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const feedback = [
    {
      id: 1,
      customer: {
        name: 'Sarah Johnson',
        email: 'sarah.j@company.com',
        avatar: ''
      },
      rating: 5,
      category: 'Product',
      subject: 'Amazing new features!',
      message: 'The latest update has made my workflow so much more efficient. Love the new dashboard!',
      date: '2024-01-15',
      status: 'New',
      source: 'In-app Survey',
      sentiment: 'Positive'
    },
    {
      id: 2,
      customer: {
        name: 'Mike Chen',
        email: 'mike.chen@business.com',
        avatar: ''
      },
      rating: 2,
      category: 'Support',
      subject: 'Response time could be better',
      message: 'Had to wait 3 days for a response to my ticket. The resolution was good but the wait time was frustrating.',
      date: '2024-01-14',
      status: 'Responded',
      source: 'Email Survey',
      sentiment: 'Negative'
    },
    {
      id: 3,
      customer: {
        name: 'Emily Davis',
        email: 'emily.d@startup.io',
        avatar: ''
      },
      rating: 4,
      category: 'UI/UX',
      subject: 'Great design, minor improvements needed',
      message: 'The interface is intuitive and clean. Would love to see more customization options for the sidebar.',
      date: '2024-01-13',
      status: 'In Review',
      source: 'Website Widget',
      sentiment: 'Positive'
    },
    {
      id: 4,
      customer: {
        name: 'David Wilson',
        email: 'david.w@enterprise.com',
        avatar: ''
      },
      rating: 1,
      category: 'Performance',
      subject: 'Slow loading times',
      message: 'The application has been very slow lately, especially during peak hours. This is impacting our team\'s productivity.',
      date: '2024-01-12',
      status: 'Escalated',
      source: 'Support Ticket',
      sentiment: 'Negative'
    },
    {
      id: 5,
      customer: {
        name: 'Lisa Park',
        email: 'lisa.park@agency.com',
        avatar: ''
      },
      rating: 5,
      category: 'Feature Request',
      subject: 'Excellent customer service',
      message: 'The support team went above and beyond to help us implement the integration. Fantastic experience!',
      date: '2024-01-11',
      status: 'Closed',
      source: 'Phone Survey',
      sentiment: 'Positive'
    }
  ];

  const surveys = [
    {
      id: 1,
      name: 'Customer Satisfaction Survey',
      type: 'CSAT',
      status: 'Active',
      responses: 1250,
      avgRating: 4.2,
      completionRate: 67.8,
      lastSent: '2024-01-15'
    },
    {
      id: 2,
      name: 'Net Promoter Score',
      type: 'NPS',
      status: 'Active',
      responses: 890,
      avgRating: 8.1,
      completionRate: 54.2,
      lastSent: '2024-01-10'
    },
    {
      id: 3,
      name: 'Product Feature Feedback',
      type: 'Product',
      status: 'Draft',
      responses: 0,
      avgRating: 0,
      completionRate: 0,
      lastSent: null
    },
    {
      id: 4,
      name: 'Support Experience Survey',
      type: 'Support',
      status: 'Paused',
      responses: 345,
      avgRating: 3.8,
      completionRate: 72.1,
      lastSent: '2024-01-05'
    }
  ];

  const insights = [
    {
      category: 'Product',
      positiveCount: 45,
      negativeCount: 12,
      sentiment: 78.9,
      trending: 'up'
    },
    {
      category: 'Support',
      positiveCount: 23,
      negativeCount: 18,
      sentiment: 56.1,
      trending: 'down'
    },
    {
      category: 'UI/UX',
      positiveCount: 38,
      negativeCount: 8,
      sentiment: 82.6,
      trending: 'up'
    },
    {
      category: 'Performance',
      positiveCount: 15,
      negativeCount: 25,
      sentiment: 37.5,
      trending: 'down'
    }
  ];

  const getRatingColor = (rating: number) => {
    if (rating >= 4) return 'text-green-500';
    if (rating >= 3) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'New': return 'default';
      case 'In Review': return 'secondary';
      case 'Responded': return 'outline';
      case 'Escalated': return 'destructive';
      case 'Closed': return 'secondary';
      default: return 'outline';
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'Positive': return 'text-green-500';
      case 'Negative': return 'text-red-500';
      case 'Neutral': return 'text-yellow-500';
      default: return 'text-gray-500';
    }
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, index) => (
      <Star
        key={index}
        className={`h-4 w-4 ${
          index < rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'
        }`}
      />
    ));
  };

  const filteredFeedback = feedback.filter(item => {
    const matchesSearch = item.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.customer.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRating = selectedRating === 'all' || item.rating.toString() === selectedRating;
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    
    return matchesSearch && matchesRating && matchesCategory;
  });

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Customer Feedback</h1>
          <p className="text-muted-foreground">
            Collect and manage customer feedback
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <BarChart3 className="mr-2 h-4 w-4" />
            Analytics
          </Button>
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                New Survey
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Create Feedback Survey</DialogTitle>
                <DialogDescription>
                  Create a new customer feedback survey
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="survey-name" className="text-right">Name</Label>
                  <Input id="survey-name" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="survey-type" className="text-right">Type</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select survey type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="csat">Customer Satisfaction (CSAT)</SelectItem>
                      <SelectItem value="nps">Net Promoter Score (NPS)</SelectItem>
                      <SelectItem value="product">Product Feedback</SelectItem>
                      <SelectItem value="support">Support Experience</SelectItem>
                      <SelectItem value="custom">Custom Survey</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="audience" className="text-right">Audience</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select target audience" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all-customers">All Customers</SelectItem>
                      <SelectItem value="recent-customers">Recent Customers</SelectItem>
                      <SelectItem value="support-contacts">Support Contacts</SelectItem>
                      <SelectItem value="trial-users">Trial Users</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="description" className="text-right">Description</Label>
                  <Textarea id="description" className="col-span-3" />
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Save Draft
                </Button>
                <Button onClick={() => setIsCreateDialogOpen(false)}>
                  Create Survey
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Feedback Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Feedback</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{feedback.length}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+12</span> this week
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Rating</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(feedback.reduce((sum, item) => sum + item.rating, 0) / feedback.length).toFixed(1)}
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+0.2</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Positive Sentiment</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round((feedback.filter(item => item.sentiment === 'Positive').length / feedback.length) * 100)}%
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+5%</span> improvement
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Response Rate</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">68.4%</div>
            <p className="text-xs text-muted-foreground">
              Survey completion rate
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="feedback" className="space-y-4">
        <TabsList>
          <TabsTrigger value="feedback">Feedback</TabsTrigger>
          <TabsTrigger value="surveys">Surveys</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
        </TabsList>

        <TabsContent value="feedback" className="space-y-4">
          {/* Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <Input
                      placeholder="Search feedback..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <Select value={selectedRating} onValueChange={setSelectedRating}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Ratings</SelectItem>
                    <SelectItem value="5">5 Stars</SelectItem>
                    <SelectItem value="4">4 Stars</SelectItem>
                    <SelectItem value="3">3 Stars</SelectItem>
                    <SelectItem value="2">2 Stars</SelectItem>
                    <SelectItem value="1">1 Star</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    <SelectItem value="Product">Product</SelectItem>
                    <SelectItem value="Support">Support</SelectItem>
                    <SelectItem value="UI/UX">UI/UX</SelectItem>
                    <SelectItem value="Performance">Performance</SelectItem>
                    <SelectItem value="Feature Request">Feature Request</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Feedback List */}
          <Card>
            <CardHeader>
              <CardTitle>Customer Feedback</CardTitle>
              <CardDescription>
                {filteredFeedback.length} feedback items found
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredFeedback.map((item) => (
                  <div key={item.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-start gap-3">
                        <Avatar>
                          <AvatarImage src={item.customer.avatar} />
                          <AvatarFallback>
                            {item.customer.name.split(' ').map(n => n[0]).join('')}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <h3 className="font-medium">{item.customer.name}</h3>
                          <p className="text-sm text-muted-foreground">{item.customer.email}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <div className="flex">{renderStars(item.rating)}</div>
                            <Badge variant="outline" className="text-xs">
                              {item.category}
                            </Badge>
                            <Badge variant={getStatusColor(item.status)} className="text-xs">
                              {item.status}
                            </Badge>
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-muted-foreground">{item.date}</div>
                        <div className="text-sm text-muted-foreground">{item.source}</div>
                        <div className={`text-sm font-medium ${getSentimentColor(item.sentiment)}`}>
                          {item.sentiment}
                        </div>
                      </div>
                    </div>
                    <div className="mb-3">
                      <h4 className="font-medium mb-1">{item.subject}</h4>
                      <p className="text-sm text-muted-foreground">{item.message}</p>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        Respond
                      </Button>
                      <Button variant="outline" size="sm">
                        View Details
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="surveys" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Feedback Surveys</CardTitle>
              <CardDescription>
                Manage your customer feedback surveys
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Survey</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Responses</TableHead>
                    <TableHead>Performance</TableHead>
                    <TableHead>Last Sent</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {surveys.map((survey) => (
                    <TableRow key={survey.id}>
                      <TableCell>
                        <div className="font-medium">{survey.name}</div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{survey.type}</Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusColor(survey.status)}>
                          {survey.status}
                        </Badge>
                      </TableCell>
                      <TableCell>{survey.responses}</TableCell>
                      <TableCell>
                        <div>
                          <div className="text-sm">
                            Avg Rating: <span className={getRatingColor(survey.avgRating)}>{survey.avgRating}</span>
                          </div>
                          <div className="text-sm text-muted-foreground">
                            Completion: {survey.completionRate}%
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        {survey.lastSent || <span className="text-muted-foreground">Never</span>}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="outline" size="sm">
                            Edit
                          </Button>
                          <Button variant="outline" size="sm">
                            Send
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

        <TabsContent value="insights" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Feedback Insights</CardTitle>
              <CardDescription>
                Sentiment analysis and trends by category
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {insights.map((insight, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-medium">{insight.category}</h3>
                      <div className="flex items-center gap-2">
                        {insight.trending === 'up' ? (
                          <TrendingUp className="h-4 w-4 text-green-500" />
                        ) : (
                          <TrendingDown className="h-4 w-4 text-red-500" />
                        )}
                        <span className="text-sm font-medium">{insight.sentiment}%</span>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Positive: {insight.positiveCount}</span>
                        <span>Negative: {insight.negativeCount}</span>
                      </div>
                      <Progress value={insight.sentiment} className="h-2" />
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