import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Badge } from '../../components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { Separator } from '../../components/ui/separator';
import { ScrollArea } from '../../components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { MessageSquare, Send, Phone, Video, MoreHorizontal, Clock, Users, TrendingUp, Zap, User, Bot, Settings } from 'lucide-react';
import { useState } from 'react';

export function LiveChatPage() {
  const [selectedChat, setSelectedChat] = useState<number | null>(1);
  const [messageInput, setMessageInput] = useState('');

  const activeChats = [
    {
      id: 1,
      customer: {
        name: 'Sarah Johnson',
        email: 'sarah.j@example.com',
        avatar: '',
        status: 'online'
      },
      lastMessage: 'I need help with setting up my account',
      timestamp: '2 min ago',
      unread: 3,
      priority: 'high',
      agent: 'John Smith'
    },
    {
      id: 2,
      customer: {
        name: 'Mike Chen',
        email: 'mike.chen@company.com',
        avatar: '',
        status: 'away'
      },
      lastMessage: 'When will the new feature be available?',
      timestamp: '5 min ago',
      unread: 1,
      priority: 'medium',
      agent: 'Emily Davis'
    },
    {
      id: 3,
      customer: {
        name: 'Lisa Park',
        email: 'lisa.park@business.com',
        avatar: '',
        status: 'online'
      },
      lastMessage: 'Thank you for your help!',
      timestamp: '12 min ago',
      unread: 0,
      priority: 'low',
      agent: 'John Smith'
    }
  ];

  const currentChat = activeChats.find(chat => chat.id === selectedChat);

  const messages = [
    {
      id: 1,
      sender: 'customer',
      content: 'Hi, I need help with setting up my account',
      timestamp: '2:30 PM',
      type: 'text'
    },
    {
      id: 2,
      sender: 'agent',
      content: 'Hello! I\'d be happy to help you set up your account. What specific issue are you encountering?',
      timestamp: '2:31 PM',
      type: 'text'
    },
    {
      id: 3,
      sender: 'customer',
      content: 'I\'m having trouble with the two-factor authentication setup',
      timestamp: '2:32 PM',
      type: 'text'
    },
    {
      id: 4,
      sender: 'agent',
      content: 'I can guide you through the 2FA setup process. Let me share a quick guide with you.',
      timestamp: '2:33 PM',
      type: 'text'
    },
    {
      id: 5,
      sender: 'bot',
      content: 'Here\'s a helpful article about 2FA setup: [Two-Factor Authentication Guide]',
      timestamp: '2:33 PM',
      type: 'link'
    }
  ];

  const agents = [
    {
      name: 'John Smith',
      status: 'online',
      activeChats: 3,
      avatar: ''
    },
    {
      name: 'Emily Davis',
      status: 'online',
      activeChats: 2,
      avatar: ''
    },
    {
      name: 'Mike Wilson',
      status: 'away',
      activeChats: 1,
      avatar: ''
    },
    {
      name: 'Sarah Brown',
      status: 'offline',
      activeChats: 0,
      avatar: ''
    }
  ];

  const chatStats = [
    {
      title: 'Active Chats',
      value: activeChats.length.toString(),
      change: '+2',
      icon: MessageSquare
    },
    {
      title: 'Avg Response Time',
      value: '45s',
      change: '-12s',
      icon: Clock
    },
    {
      title: 'Online Agents',
      value: agents.filter(agent => agent.status === 'online').length.toString(),
      change: '+1',
      icon: Users
    },
    {
      title: 'Satisfaction Rate',
      value: '94%',
      change: '+2%',
      icon: TrendingUp
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'away': return 'bg-yellow-500';
      case 'offline': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'destructive';
      case 'medium': return 'secondary';
      case 'low': return 'outline';
      default: return 'outline';
    }
  };

  const handleSendMessage = () => {
    if (messageInput.trim()) {
      // Add message logic here
      setMessageInput('');
    }
  };

  return (
    <div className="h-[calc(100vh-2rem)] p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1>Live Chat</h1>
          <p className="text-muted-foreground">
            Real-time customer support chat system
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Settings className="mr-2 h-4 w-4" />
            Settings
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {chatStats.map((stat, index) => {
          const IconComponent = stat.icon;
          return (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <IconComponent className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">
                  <span className="text-green-500">{stat.change}</span> from yesterday
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Main Chat Interface */}
      <div className="grid grid-cols-12 gap-6 h-[600px]">
        {/* Chat List */}
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              Active Chats
              <Badge variant="secondary">{activeChats.length}</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <ScrollArea className="h-[500px]">
              <div className="space-y-2 p-4">
                {activeChats.map((chat) => (
                  <div
                    key={chat.id}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedChat === chat.id ? 'bg-primary/10' : 'hover:bg-muted'
                    }`}
                    onClick={() => setSelectedChat(chat.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3">
                        <div className="relative">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={chat.customer.avatar} />
                            <AvatarFallback>
                              {chat.customer.name.split(' ').map(n => n[0]).join('')}
                            </AvatarFallback>
                          </Avatar>
                          <div className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-background ${getStatusColor(chat.customer.status)}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-medium truncate">{chat.customer.name}</p>
                            <span className="text-xs text-muted-foreground">{chat.timestamp}</span>
                          </div>
                          <p className="text-xs text-muted-foreground truncate">{chat.lastMessage}</p>
                          <div className="flex items-center justify-between mt-1">
                            <Badge variant={getPriorityColor(chat.priority)} className="text-xs">
                              {chat.priority}
                            </Badge>
                            {chat.unread > 0 && (
                              <Badge variant="destructive" className="text-xs">
                                {chat.unread}
                              </Badge>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Chat Window */}
        <Card className="col-span-6">
          {currentChat ? (
            <div className="flex flex-col h-full">
              {/* Chat Header */}
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src={currentChat.customer.avatar} />
                      <AvatarFallback>
                        {currentChat.customer.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="font-medium">{currentChat.customer.name}</h3>
                      <p className="text-sm text-muted-foreground">{currentChat.customer.email}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                      <Phone className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <Video className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <Separator />

              {/* Messages */}
              <CardContent className="flex-1 p-0">
                <ScrollArea className="h-[380px] p-4">
                  <div className="space-y-4">
                    {messages.map((message) => (
                      <div
                        key={message.id}
                        className={`flex ${message.sender === 'agent' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div className={`max-w-[70%] p-3 rounded-lg ${
                          message.sender === 'agent'
                            ? 'bg-primary text-primary-foreground'
                            : message.sender === 'bot'
                            ? 'bg-muted border'
                            : 'bg-muted'
                        }`}>
                          {message.sender === 'bot' && (
                            <div className="flex items-center gap-2 mb-1">
                              <Bot className="h-3 w-3" />
                              <span className="text-xs font-medium">Bot</span>
                            </div>
                          )}
                          <p className="text-sm">{message.content}</p>
                          <p className={`text-xs mt-1 ${
                            message.sender === 'agent' ? 'text-primary-foreground/70' : 'text-muted-foreground'
                          }`}>
                            {message.timestamp}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>

              {/* Message Input */}
              <div className="p-4 border-t">
                <div className="flex gap-2">
                  <Input
                    placeholder="Type your message..."
                    value={messageInput}
                    onChange={(e) => setMessageInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    className="flex-1"
                  />
                  <Button onClick={handleSendMessage}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <MessageSquare className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                <h3 className="font-medium mb-2">Select a chat to start messaging</h3>
                <p className="text-sm text-muted-foreground">
                  Choose a conversation from the left to view messages
                </p>
              </div>
            </div>
          )}
        </Card>

        {/* Agent Panel */}
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Team Status</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <ScrollArea className="h-[500px]">
              <div className="space-y-3 p-4">
                {agents.map((agent, index) => (
                  <div key={index} className="flex items-center justify-between p-2 rounded">
                    <div className="flex items-center space-x-2">
                      <div className="relative">
                        <Avatar className="h-8 w-8">
                          <AvatarImage src={agent.avatar} />
                          <AvatarFallback>
                            {agent.name.split(' ').map(n => n[0]).join('')}
                          </AvatarFallback>
                        </Avatar>
                        <div className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-background ${getStatusColor(agent.status)}`} />
                      </div>
                      <div>
                        <p className="text-sm font-medium">{agent.name}</p>
                        <p className="text-xs text-muted-foreground capitalize">{agent.status}</p>
                      </div>
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      {agent.activeChats}
                    </Badge>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}