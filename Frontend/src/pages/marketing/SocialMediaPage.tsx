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
import { Plus, Calendar, BarChart3, Users, Heart, MessageSquare, Share, Eye, TrendingUp, Facebook, Twitter, Instagram, Linkedin, Image } from 'lucide-react';
import { useState } from 'react';

export function SocialMediaPage() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState('all');

  const posts = [
    {
      id: 1,
      content: 'Excited to announce our new product features! 🚀 Check out what we\'ve been working on...',
      platform: 'Twitter',
      status: 'Published',
      scheduledDate: '2024-01-15 10:00',
      metrics: {
        likes: 234,
        comments: 45,
        shares: 67,
        views: 1250
      },
      engagement: 6.8
    },
    {
      id: 2,
      content: 'Behind the scenes: Our team working hard to deliver the best experience for our customers.',
      platform: 'LinkedIn',
      status: 'Scheduled',
      scheduledDate: '2024-01-18 14:30',
      metrics: {
        likes: 0,
        comments: 0,
        shares: 0,
        views: 0
      },
      engagement: 0
    },
    {
      id: 3,
      content: 'Customer success story: How Company X increased their productivity by 40% using our platform.',
      platform: 'Facebook',
      status: 'Published',
      scheduledDate: '2024-01-14 12:00',
      metrics: {
        likes: 189,
        comments: 28,
        shares: 34,
        views: 890
      },
      engagement: 5.2
    },
    {
      id: 4,
      content: 'Join us for our upcoming webinar on industry best practices. Limited seats available!',
      platform: 'Instagram',
      status: 'Draft',
      scheduledDate: null,
      metrics: {
        likes: 0,
        comments: 0,
        shares: 0,
        views: 0
      },
      engagement: 0
    }
  ];

  const accounts = [
    {
      platform: 'Twitter',
      username: '@company',
      followers: 12500,
      following: 850,
      posts: 1240,
      engagement: 4.2,
      connected: true,
      icon: Twitter
    },
    {
      platform: 'LinkedIn',
      username: 'Company Page',
      followers: 8900,
      following: 200,
      posts: 340,
      engagement: 6.8,
      connected: true,
      icon: Linkedin
    },
    {
      platform: 'Facebook',
      username: 'Company',
      followers: 15600,
      following: 120,
      posts: 890,
      engagement: 3.1,
      connected: true,
      icon: Facebook
    },
    {
      platform: 'Instagram',
      username: '@company_official',
      followers: 22300,
      following: 450,
      posts: 567,
      engagement: 7.5,
      connected: false,
      icon: Instagram
    }
  ];

  const analytics = [
    { platform: 'Twitter', reach: 45200, engagement: 1890, clicks: 234, followers: 156 },
    { platform: 'LinkedIn', reach: 23400, engagement: 1560, clicks: 189, followers: 89 },
    { platform: 'Facebook', reach: 38900, engagement: 1234, clicks: 167, followers: 112 },
    { platform: 'Instagram', reach: 52100, engagement: 3910, clicks: 445, followers: 234 }
  ];

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'Twitter': return <Twitter className="h-4 w-4 text-blue-400" />;
      case 'LinkedIn': return <Linkedin className="h-4 w-4 text-blue-600" />;
      case 'Facebook': return <Facebook className="h-4 w-4 text-blue-700" />;
      case 'Instagram': return <Instagram className="h-4 w-4 text-pink-500" />;
      default: return <Share className="h-4 w-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Published': return 'default';
      case 'Scheduled': return 'secondary';
      case 'Draft': return 'outline';
      default: return 'outline';
    }
  };

  const filteredPosts = posts.filter(post => {
    if (selectedPlatform === 'all') return true;
    return post.platform === selectedPlatform;
  });

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Social Media</h1>
          <p className="text-muted-foreground">
            Manage social media presence and campaigns
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
                Create Post
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Create Social Media Post</DialogTitle>
                <DialogDescription>
                  Create and schedule a new social media post
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="platform" className="text-right">Platform</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select platform" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="twitter">Twitter</SelectItem>
                      <SelectItem value="linkedin">LinkedIn</SelectItem>
                      <SelectItem value="facebook">Facebook</SelectItem>
                      <SelectItem value="instagram">Instagram</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="content" className="text-right">Content</Label>
                  <Textarea 
                    id="content" 
                    placeholder="What's happening?"
                    className="col-span-3 min-h-[100px]" 
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="media" className="text-right">Media</Label>
                  <Button variant="outline" className="col-span-3 justify-start">
                    <Image className="mr-2 h-4 w-4" />
                    Add Image/Video
                  </Button>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="schedule" className="text-right">Schedule</Label>
                  <Select>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Post now or schedule" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="now">Post Now</SelectItem>
                      <SelectItem value="schedule">Schedule for Later</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Save Draft
                </Button>
                <Button onClick={() => setIsCreateDialogOpen(false)}>
                  Post Now
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Social Media Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Followers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {accounts.reduce((sum, account) => sum + account.followers, 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+8.2%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Reach</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">159.6K</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+12.1%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Engagement</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8.6K</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-500">+15.3%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Engagement Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5.4%</div>
            <p className="text-xs text-muted-foreground">
              Industry avg: 3.2%
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="posts" className="space-y-4">
        <TabsList>
          <TabsTrigger value="posts">Posts</TabsTrigger>
          <TabsTrigger value="accounts">Accounts</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="scheduler">Scheduler</TabsTrigger>
        </TabsList>

        <TabsContent value="posts" className="space-y-4">
          {/* Post Filters */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex gap-4">
                <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Platforms</SelectItem>
                    <SelectItem value="Twitter">Twitter</SelectItem>
                    <SelectItem value="LinkedIn">LinkedIn</SelectItem>
                    <SelectItem value="Facebook">Facebook</SelectItem>
                    <SelectItem value="Instagram">Instagram</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Posts List */}
          <Card>
            <CardHeader>
              <CardTitle>Social Media Posts</CardTitle>
              <CardDescription>
                {filteredPosts.length} posts found
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredPosts.map((post) => (
                  <div key={post.id} className="flex items-start justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        {getPlatformIcon(post.platform)}
                        <span className="font-medium">{post.platform}</span>
                        <Badge variant={getStatusColor(post.status)}>
                          {post.status}
                        </Badge>
                      </div>
                      <p className="text-sm mb-3 max-w-2xl">{post.content}</p>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        {post.status === 'Published' ? (
                          <>
                            <span className="flex items-center gap-1">
                              <Heart className="h-3 w-3" />
                              {post.metrics.likes}
                            </span>
                            <span className="flex items-center gap-1">
                              <MessageSquare className="h-3 w-3" />
                              {post.metrics.comments}
                            </span>
                            <span className="flex items-center gap-1">
                              <Share className="h-3 w-3" />
                              {post.metrics.shares}
                            </span>
                            <span className="flex items-center gap-1">
                              <Eye className="h-3 w-3" />
                              {post.metrics.views}
                            </span>
                            <span>Engagement: {post.engagement}%</span>
                          </>
                        ) : (
                          <span>
                            {post.scheduledDate ? `Scheduled for ${post.scheduledDate}` : 'Draft'}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        Edit
                      </Button>
                      {post.status === 'Draft' && (
                        <Button size="sm">
                          Publish
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="accounts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Connected Accounts</CardTitle>
              <CardDescription>
                Manage your social media account connections
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {accounts.map((account, index) => {
                  const IconComponent = account.icon;
                  return (
                    <Card key={index} className={`${account.connected ? 'border-green-200' : 'border-gray-200'}`}>
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <IconComponent className="h-6 w-6" />
                            <div>
                              <h3 className="font-medium">{account.platform}</h3>
                              <p className="text-sm text-muted-foreground">{account.username}</p>
                            </div>
                          </div>
                          <Badge variant={account.connected ? 'default' : 'secondary'}>
                            {account.connected ? 'Connected' : 'Not Connected'}
                          </Badge>
                        </div>
                      </CardHeader>
                      <CardContent>
                        {account.connected ? (
                          <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span>Followers:</span>
                              <span>{account.followers.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span>Posts:</span>
                              <span>{account.posts.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span>Engagement:</span>
                              <span>{account.engagement}%</span>
                            </div>
                            <Button variant="outline" size="sm" className="w-full mt-3">
                              Manage Account
                            </Button>
                          </div>
                        ) : (
                          <Button className="w-full">
                            Connect Account
                          </Button>
                        )}
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Platform Analytics</CardTitle>
              <CardDescription>
                Performance metrics across all platforms
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Platform</TableHead>
                    <TableHead>Reach</TableHead>
                    <TableHead>Engagement</TableHead>
                    <TableHead>Clicks</TableHead>
                    <TableHead>New Followers</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {analytics.map((platform, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getPlatformIcon(platform.platform)}
                          {platform.platform}
                        </div>
                      </TableCell>
                      <TableCell>{platform.reach.toLocaleString()}</TableCell>
                      <TableCell>{platform.engagement.toLocaleString()}</TableCell>
                      <TableCell>{platform.clicks}</TableCell>
                      <TableCell>
                        <span className="text-green-500">+{platform.followers}</span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="scheduler" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Content Scheduler</CardTitle>
              <CardDescription>
                Schedule posts across all your social media platforms
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Calendar className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                <h3 className="font-medium mb-2">Content Calendar Coming Soon</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Plan and schedule your social media content with our visual calendar
                </p>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  Schedule New Post
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}