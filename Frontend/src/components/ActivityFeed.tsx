import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Avatar, AvatarImage, AvatarFallback } from './ui/avatar';
import { ScrollArea } from './ui/scroll-area';
import { Mail, Phone, Calendar, DollarSign, User, Clock, MoreVertical, Eye, Filter } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { useState } from 'react';

interface Activity {
  id: string;
  type: 'email' | 'call' | 'meeting' | 'deal' | 'contact';
  title: string;
  description: string;
  user: string;
  userAvatar?: string;
  timestamp: string;
  priority?: 'high' | 'medium' | 'low';
  status?: 'completed' | 'pending' | 'overdue';
}

interface ActivityFeedProps {
  title: string;
  activities: Activity[];
}

export function ActivityFeed({ title, activities }: ActivityFeedProps) {
  const [filter, setFilter] = useState<string>('all');
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'email': return <Mail className="w-4 h-4" />;
      case 'call': return <Phone className="w-4 h-4" />;
      case 'meeting': return <Calendar className="w-4 h-4" />;
      case 'deal': return <DollarSign className="w-4 h-4" />;
      case 'contact': return <User className="w-4 h-4" />;
      default: return <User className="w-4 h-4" />;
    }
  };

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'email': return {
        bg: 'bg-blue-100 dark:bg-blue-900/20',
        text: 'text-blue-600 dark:text-blue-400',
        border: 'border-blue-200 dark:border-blue-800'
      };
      case 'call': return {
        bg: 'bg-emerald-100 dark:bg-emerald-900/20',
        text: 'text-emerald-600 dark:text-emerald-400',
        border: 'border-emerald-200 dark:border-emerald-800'
      };
      case 'meeting': return {
        bg: 'bg-purple-100 dark:bg-purple-900/20',
        text: 'text-purple-600 dark:text-purple-400',
        border: 'border-purple-200 dark:border-purple-800'
      };
      case 'deal': return {
        bg: 'bg-amber-100 dark:bg-amber-900/20',
        text: 'text-amber-600 dark:text-amber-400',
        border: 'border-amber-200 dark:border-amber-800'
      };
      case 'contact': return {
        bg: 'bg-gray-100 dark:bg-gray-900/20',
        text: 'text-gray-600 dark:text-gray-400',
        border: 'border-gray-200 dark:border-gray-800'
      };
      default: return {
        bg: 'bg-gray-100 dark:bg-gray-900/20',
        text: 'text-gray-600 dark:text-gray-400',
        border: 'border-gray-200 dark:border-gray-800'
      };
    }
  };

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400';
      case 'medium': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'low': return 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400';
      case 'pending': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400';
      case 'overdue': return 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const toggleExpanded = (id: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedItems(newExpanded);
  };

  const filteredActivities = activities.filter(activity => {
    if (filter === 'all') return true;
    return activity.type === filter;
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="p-6 h-full bg-gradient-to-br from-card to-card/50 border-border/50 shadow-sm hover:shadow-md transition-all duration-300">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-semibold text-foreground">{title}</h3>
            <p className="text-sm text-muted-foreground">
              {filteredActivities.length} recent activities
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Filter className="w-4 h-4 mr-2" />
              Filter
            </Button>
            <Button variant="outline" size="sm">
              <Eye className="w-4 h-4 mr-2" />
              View All
            </Button>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-2 mb-6 p-1 bg-muted rounded-lg">
          {['all', 'email', 'call', 'meeting', 'deal'].map((type) => (
            <Button
              key={type}
              variant={filter === type ? 'default' : 'ghost'}
              size="sm"
              className="flex-1 h-8 text-xs capitalize"
              onClick={() => setFilter(type)}
            >
              {type}
            </Button>
          ))}
        </div>
        
        {/* Activity List */}
        <ScrollArea className="h-96">
          <div className="space-y-3">
            <AnimatePresence>
              {filteredActivities.map((activity, index) => {
                const colors = getActivityColor(activity.type);
                const isExpanded = expandedItems.has(activity.id);
                
                return (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                    className="group"
                  >
                    <div className={`p-4 rounded-xl border ${colors.border} bg-gradient-to-r ${colors.bg} hover:shadow-md transition-all duration-200 cursor-pointer`}
                         onClick={() => toggleExpanded(activity.id)}>
                      
                      {/* Main content */}
                      <div className="flex items-start gap-3">
                        <div className={`p-2.5 rounded-xl ${colors.bg} ${colors.text} border ${colors.border} shadow-sm`}>
                          {getActivityIcon(activity.type)}
                        </div>
                        
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <p className="font-semibold text-sm text-foreground group-hover:text-primary transition-colors">
                                {activity.title}
                              </p>
                              {!isExpanded && (
                                <p className="text-sm text-muted-foreground line-clamp-1">
                                  {activity.description}
                                </p>
                              )}
                            </div>
                            
                            <div className="flex items-center gap-2">
                              {activity.priority && (
                                <Badge className={`text-xs ${getPriorityColor(activity.priority)}`}>
                                  {activity.priority}
                                </Badge>
                              )}
                              {activity.status && (
                                <Badge className={`text-xs ${getStatusColor(activity.status)}`}>
                                  {activity.status}
                                </Badge>
                              )}
                              <Button variant="ghost" size="sm" className="h-6 w-6 p-0 opacity-0 group-hover:opacity-100 transition-opacity">
                                <MoreVertical className="w-3 h-3" />
                              </Button>
                            </div>
                          </div>
                          
                          {/* Expanded content */}
                          <AnimatePresence>
                            {isExpanded && (
                              <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                transition={{ duration: 0.2 }}
                              >
                                <p className="text-sm text-muted-foreground mb-3 p-3 bg-background/50 rounded-lg">
                                  {activity.description}
                                </p>
                              </motion.div>
                            )}
                          </AnimatePresence>
                          
                          {/* Footer */}
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Avatar className="w-6 h-6 border-2 border-background shadow-sm">
                                <AvatarImage src={activity.userAvatar} />
                                <AvatarFallback className="text-xs font-medium">
                                  {activity.user.split(' ').map(n => n[0]).join('')}
                                </AvatarFallback>
                              </Avatar>
                              <span className="text-xs font-medium text-muted-foreground">{activity.user}</span>
                            </div>
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              <Clock className="w-3 h-3" />
                              <span>{activity.timestamp}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        </ScrollArea>

        {/* Footer */}
        <div className="mt-4 pt-4 border-t border-border/50">
          <Button variant="outline" className="w-full">
            Load More Activities
          </Button>
        </div>
      </Card>
    </motion.div>
  );
}