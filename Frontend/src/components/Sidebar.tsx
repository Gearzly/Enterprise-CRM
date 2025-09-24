import { useState } from 'react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from './ui/collapsible';
import { Separator } from './ui/separator';
import { motion, AnimatePresence } from 'motion/react';
import { 
  BarChart3, 
  Users, 
  Target, 
  Calendar, 
  Settings, 
  User, 
  FileText,
  TrendingUp,
  MessageSquare,
  LogOut,
  ChevronDown,
  ChevronRight,
  DollarSign,
  Megaphone,
  Headphones,
  Activity,
  Contact,
  UserPlus,
  Quote,
  Crosshair,
  Mail,
  Share2,
  PenTool,
  BarChart,
  Zap,
  Layers,
  CalendarDays,
  Handshake,
  FolderOpen,
  Database,
  Ticket,
  BookOpen,
  MessageCircle,
  Phone,
  Radio,
  ThumbsUp,
  Clock,
  HardDrive,
  MonitorSpeaker,
  Globe,
  Smartphone,
  Puzzle,
  Languages,
  Menu,
  X,
  Bell,
  Search
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onViewChange: (view: string) => void;
  userRole: string;
}

export function Sidebar({ currentView, onViewChange, userRole }: SidebarProps) {
  const [openModules, setOpenModules] = useState<string[]>(['dashboard']);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const toggleModule = (moduleId: string) => {
    setOpenModules(prev => 
      prev.includes(moduleId) 
        ? prev.filter(id => id !== moduleId)
        : [...prev, moduleId]
    );
  };

  const salesSubmodules = [
    { id: 'sales/activities', label: 'Activities', icon: Activity, badge: '12' },
    { id: 'sales/contacts', label: 'Contacts', icon: Contact, badge: '248' },
    { id: 'sales/leads', label: 'Leads', icon: UserPlus, badge: '47' },
    { id: 'sales/opportunities', label: 'Opportunities', icon: Target, badge: '15' },
    { id: 'sales/quotations', label: 'Quotations', icon: Quote, badge: '8' },
    { id: 'sales/reports', label: 'Reports', icon: FileText },
    { id: 'sales/targets', label: 'Targets', icon: Crosshair },
  ];

  const marketingSubmodules = [
    { id: 'marketing/campaigns', label: 'Campaigns', icon: Megaphone, badge: '6' },
    { id: 'marketing/leads', label: 'Leads', icon: UserPlus, badge: '23' },
    { id: 'marketing/email', label: 'Email', icon: Mail, badge: '3' },
    { id: 'marketing/social-media', label: 'Social Media', icon: Share2 },
    { id: 'marketing/content', label: 'Content', icon: PenTool },
    { id: 'marketing/analytics', label: 'Analytics', icon: BarChart },
    { id: 'marketing/automation', label: 'Automation', icon: Zap, badge: 'NEW' },
    { id: 'marketing/segmentation', label: 'Segmentation', icon: Layers },
    { id: 'marketing/events', label: 'Events', icon: CalendarDays, badge: '2' },
    { id: 'marketing/partners', label: 'Partners', icon: Handshake },
    { id: 'marketing/resources', label: 'Resources', icon: FolderOpen },
    { id: 'marketing/cdp', label: 'CDP', icon: Database },
  ];

  const supportSubmodules = [
    { id: 'support/tickets', label: 'Tickets', icon: Ticket, badge: '34', priority: 'high' },
    { id: 'support/knowledge-base', label: 'Knowledge Base', icon: BookOpen, badge: '156' },
    { id: 'support/interactions', label: 'Interactions', icon: MessageCircle, badge: '89' },
    { id: 'support/live-chat', label: 'Live Chat', icon: MessageSquare, badge: '5', priority: 'active' },
    { id: 'support/call-center', label: 'Call Center', icon: Phone },
    { id: 'support/social-support', label: 'Social Support', icon: Share2, badge: '12' },
    { id: 'support/feedback', label: 'Feedback', icon: ThumbsUp, badge: '7' },
    { id: 'support/sla', label: 'SLA', icon: Clock, badge: '!', priority: 'urgent' },
    { id: 'support/asset', label: 'Asset', icon: HardDrive },
    { id: 'support/remote', label: 'Remote', icon: MonitorSpeaker },
    { id: 'support/community', label: 'Community', icon: Users },
    { id: 'support/reporting', label: 'Reporting', icon: FileText },
    { id: 'support/automation', label: 'Automation', icon: Zap },
    { id: 'support/mobile', label: 'Mobile', icon: Smartphone },
    { id: 'support/integration', label: 'Integration', icon: Puzzle },
    { id: 'support/language', label: 'Language', icon: Languages },
  ];

  const adminItems = [
    { id: 'users', label: 'User Management', icon: User, badge: '8' },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  // Filter items based on search query
  const filterItems = (items: any[]) => {
    if (!searchQuery) return items;
    return items.filter(item => 
      item.label.toLowerCase().includes(searchQuery.toLowerCase())
    );
  };

  const getRoleBadgeColor = (userRole: string) => {
    switch (userRole) {
      case 'Admin': return 'bg-red-500';
      case 'Sales Manager': return 'bg-blue-500';
      case 'Sales Rep': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getBadgeVariant = (priority?: string) => {
    switch (priority) {
      case 'urgent': return 'destructive';
      case 'high': return 'secondary';
      case 'active': return 'default';
      default: return 'outline';
    }
  };

  return (
    <TooltipProvider>
      <motion.div 
        className={`${isCollapsed ? 'w-16' : 'w-72'} bg-sidebar border-r border-sidebar-border h-screen flex flex-col shadow-lg transition-all duration-300`}
        initial={false}
        animate={{ width: isCollapsed ? 64 : 288 }}
      >
        {/* Header */}
        <div className="p-4 border-b border-sidebar-border bg-sidebar">
          <div className="flex items-center justify-between">
            {!isCollapsed && (
              <motion.div 
                className="flex-1"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <h1 className="text-xl font-semibold text-sidebar-foreground">CRM System</h1>
                <div className="flex items-center gap-2 mt-1">
                  <div className={`w-2 h-2 rounded-full ${getRoleBadgeColor(userRole)}`} />
                  <p className="text-sm text-sidebar-foreground/70">{userRole}</p>
                  <Badge variant="outline" className="text-xs">Online</Badge>
                </div>
              </motion.div>
            )}
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="text-sidebar-foreground hover:bg-sidebar-accent h-8 w-8 p-0"
            >
              {isCollapsed ? <Menu className="w-4 h-4" /> : <X className="w-4 h-4" />}
            </Button>
          </div>
          
          {/* Search Bar */}
          {!isCollapsed && (
            <motion.div 
              className="mt-4"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-sidebar-foreground/50" />
                <input
                  type="text"
                  placeholder="Search navigation..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 text-sm bg-sidebar-accent border border-sidebar-border rounded-lg focus:ring-2 focus:ring-sidebar-ring focus:border-transparent transition-all"
                />
              </div>
            </motion.div>
          )}
        </div>
      
      <nav className="flex-1 p-3 overflow-y-auto">
        <div className="space-y-1">
          {/* Dashboard */}
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant={currentView === 'dashboard' ? "default" : "ghost"}
                className={`w-full ${isCollapsed ? 'justify-center px-0' : 'justify-start'} h-10 relative group transition-all hover:scale-[1.02]`}
                onClick={() => onViewChange('dashboard')}
              >
                <BarChart3 className={`w-5 h-5 ${isCollapsed ? '' : 'mr-3'}`} />
                {!isCollapsed && (
                  <motion.span
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -10 }}
                  >
                    Dashboard
                  </motion.span>
                )}
                {currentView === 'dashboard' && (
                  <motion.div
                    className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                    layoutId="activeIndicator"
                  />
                )}
              </Button>
            </TooltipTrigger>
            {isCollapsed && <TooltipContent side="right">Dashboard</TooltipContent>}
          </Tooltip>

          {!isCollapsed && <Separator className="my-4" />}

          {/* Sales Module */}
          <div className="space-y-1">
            {!isCollapsed && (
              <motion.p 
                className="px-3 py-2 text-xs font-medium text-sidebar-foreground/50 uppercase tracking-wider"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
              >
                Modules
              </motion.p>
            )}
            
            <Collapsible open={openModules.includes('sales')} onOpenChange={() => toggleModule('sales')}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <CollapsibleTrigger asChild>
                    <Button 
                      variant="ghost" 
                      className={`w-full ${isCollapsed ? 'justify-center px-0' : 'justify-start'} h-10 group relative`}
                    >
                      {!isCollapsed && (
                        <motion.div
                          animate={{ rotate: openModules.includes('sales') ? 90 : 0 }}
                          transition={{ duration: 0.2 }}
                          className="mr-2"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </motion.div>
                      )}
                      <DollarSign className={`w-5 h-5 ${isCollapsed ? '' : 'mr-2'}`} />
                      {!isCollapsed && (
                        <motion.span
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                        >
                          Sales
                        </motion.span>
                      )}
                    </Button>
                  </CollapsibleTrigger>
                </TooltipTrigger>
                {isCollapsed && <TooltipContent side="right">Sales</TooltipContent>}
              </Tooltip>
              
              {!isCollapsed && (
                <AnimatePresence>
                  {openModules.includes('sales') && (
                    <CollapsibleContent asChild>
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.2 }}
                        className="ml-6 space-y-1 mt-1"
                      >
                        {filterItems(salesSubmodules).map((item, index) => {
                          const IconComponent = item.icon;
                          return (
                            <motion.div
                              key={item.id}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.05 }}
                            >
                              <Button
                                variant={currentView === item.id ? "default" : "ghost"}
                                className="w-full justify-start text-sm h-9 relative group"
                                onClick={() => onViewChange(item.id)}
                              >
                                <IconComponent className="w-4 h-4 mr-3" />
                                <span className="flex-1 text-left">{item.label}</span>
                                {item.badge && (
                                  <Badge 
                                    variant={getBadgeVariant(item.priority)} 
                                    className="text-xs h-5 min-w-[20px] px-1.5"
                                  >
                                    {item.badge}
                                  </Badge>
                                )}
                                {currentView === item.id && (
                                  <motion.div
                                    className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                                    layoutId="activeIndicatorSub"
                                  />
                                )}
                              </Button>
                            </motion.div>
                          );
                        })}
                      </motion.div>
                    </CollapsibleContent>
                  )}
                </AnimatePresence>
              )}
            </Collapsible>
          </div>

          {/* Marketing Module */}
          <div className="space-y-1">
            <Collapsible open={openModules.includes('marketing')} onOpenChange={() => toggleModule('marketing')}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <CollapsibleTrigger asChild>
                    <Button 
                      variant="ghost" 
                      className={`w-full ${isCollapsed ? 'justify-center px-0' : 'justify-start'} h-10 group relative`}
                    >
                      {!isCollapsed && (
                        <motion.div
                          animate={{ rotate: openModules.includes('marketing') ? 90 : 0 }}
                          transition={{ duration: 0.2 }}
                          className="mr-2"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </motion.div>
                      )}
                      <Megaphone className={`w-5 h-5 ${isCollapsed ? '' : 'mr-2'}`} />
                      {!isCollapsed && (
                        <motion.span
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                        >
                          Marketing
                        </motion.span>
                      )}
                    </Button>
                  </CollapsibleTrigger>
                </TooltipTrigger>
                {isCollapsed && <TooltipContent side="right">Marketing</TooltipContent>}
              </Tooltip>
              
              {!isCollapsed && (
                <AnimatePresence>
                  {openModules.includes('marketing') && (
                    <CollapsibleContent asChild>
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.2 }}
                        className="ml-6 space-y-1 mt-1"
                      >
                        {filterItems(marketingSubmodules).map((item, index) => {
                          const IconComponent = item.icon;
                          return (
                            <motion.div
                              key={item.id}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.05 }}
                            >
                              <Button
                                variant={currentView === item.id ? "default" : "ghost"}
                                className="w-full justify-start text-sm h-9 relative group"
                                onClick={() => onViewChange(item.id)}
                              >
                                <IconComponent className="w-4 h-4 mr-3" />
                                <span className="flex-1 text-left">{item.label}</span>
                                {item.badge && (
                                  <Badge 
                                    variant={getBadgeVariant(item.priority)} 
                                    className="text-xs h-5 min-w-[20px] px-1.5"
                                  >
                                    {item.badge}
                                  </Badge>
                                )}
                                {currentView === item.id && (
                                  <motion.div
                                    className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                                    layoutId="activeIndicatorSub"
                                  />
                                )}
                              </Button>
                            </motion.div>
                          );
                        })}
                      </motion.div>
                    </CollapsibleContent>
                  )}
                </AnimatePresence>
              )}
            </Collapsible>
          </div>

          {/* Support Module */}
          <div className="space-y-1">
            <Collapsible open={openModules.includes('support')} onOpenChange={() => toggleModule('support')}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <CollapsibleTrigger asChild>
                    <Button 
                      variant="ghost" 
                      className={`w-full ${isCollapsed ? 'justify-center px-0' : 'justify-start'} h-10 group relative`}
                    >
                      {!isCollapsed && (
                        <motion.div
                          animate={{ rotate: openModules.includes('support') ? 90 : 0 }}
                          transition={{ duration: 0.2 }}
                          className="mr-2"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </motion.div>
                      )}
                      <Headphones className={`w-5 h-5 ${isCollapsed ? '' : 'mr-2'}`} />
                      {!isCollapsed && (
                        <motion.span
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                        >
                          Support
                        </motion.span>
                      )}
                      {/* Urgent badge for support */}
                      {!isCollapsed && (
                        <Badge variant="destructive" className="ml-auto text-xs h-5">
                          !
                        </Badge>
                      )}
                    </Button>
                  </CollapsibleTrigger>
                </TooltipTrigger>
                {isCollapsed && <TooltipContent side="right">Support</TooltipContent>}
              </Tooltip>
              
              {!isCollapsed && (
                <AnimatePresence>
                  {openModules.includes('support') && (
                    <CollapsibleContent asChild>
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.2 }}
                        className="ml-6 space-y-1 mt-1"
                      >
                        {filterItems(supportSubmodules).map((item, index) => {
                          const IconComponent = item.icon;
                          return (
                            <motion.div
                              key={item.id}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.05 }}
                            >
                              <Button
                                variant={currentView === item.id ? "default" : "ghost"}
                                className="w-full justify-start text-sm h-9 relative group"
                                onClick={() => onViewChange(item.id)}
                              >
                                <IconComponent className="w-4 h-4 mr-3" />
                                <span className="flex-1 text-left">{item.label}</span>
                                {item.badge && (
                                  <Badge 
                                    variant={getBadgeVariant(item.priority)} 
                                    className="text-xs h-5 min-w-[20px] px-1.5"
                                  >
                                    {item.badge}
                                  </Badge>
                                )}
                                {currentView === item.id && (
                                  <motion.div
                                    className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                                    layoutId="activeIndicatorSub"
                                  />
                                )}
                              </Button>
                            </motion.div>
                          );
                        })}
                      </motion.div>
                    </CollapsibleContent>
                  )}
                </AnimatePresence>
              )}
            </Collapsible>
          </div>
          
          {/* Administration */}
          {(userRole === 'Admin' || userRole === 'Sales Manager') && (
            <>
              {!isCollapsed && <Separator className="my-4" />}
              {!isCollapsed && (
                <motion.p 
                  className="px-3 py-2 text-xs font-medium text-sidebar-foreground/50 uppercase tracking-wider"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                >
                  Administration
                </motion.p>
              )}
              <div className="space-y-1">
                {adminItems.map((item, index) => {
                  const IconComponent = item.icon;
                  return (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Button
                            variant={currentView === item.id ? "default" : "ghost"}
                            className={`w-full ${isCollapsed ? 'justify-center px-0' : 'justify-start'} h-10 relative group transition-all hover:scale-[1.02]`}
                            onClick={() => onViewChange(item.id)}
                          >
                            <IconComponent className={`w-5 h-5 ${isCollapsed ? '' : 'mr-3'}`} />
                            {!isCollapsed && (
                              <motion.span
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="flex-1 text-left"
                              >
                                {item.label}
                              </motion.span>
                            )}
                            {!isCollapsed && item.badge && (
                              <Badge variant="outline" className="text-xs h-5 min-w-[20px] px-1.5">
                                {item.badge}
                              </Badge>
                            )}
                            {currentView === item.id && (
                              <motion.div
                                className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                                layoutId="activeIndicator"
                              />
                            )}
                          </Button>
                        </TooltipTrigger>
                        {isCollapsed && <TooltipContent side="right">{item.label}</TooltipContent>}
                      </Tooltip>
                    </motion.div>
                  );
                })}
              </div>
            </>
          )}
        </div>
      </nav>
      
      {/* Footer */}
      <div className="p-3 border-t border-sidebar-border bg-sidebar">
        {!isCollapsed && (
          <div className="mb-3 px-2">
            <div className="flex items-center gap-2 text-xs text-sidebar-foreground/50">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span>System Status: Online</span>
            </div>
          </div>
        )}
        
        <div className="flex items-center gap-2">
          {!isCollapsed && (
            <Button variant="ghost" size="sm" className="flex-1 justify-start text-destructive hover:text-destructive hover:bg-red-50">
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </Button>
          )}
          
          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant="ghost" size="sm" className={`${isCollapsed ? 'w-full' : ''} hover:bg-sidebar-accent`}>
                <Bell className={`w-4 h-4 ${isCollapsed ? '' : 'mr-2'}`} />
                {!isCollapsed && 'Notifications'}
                <Badge className="ml-auto h-4 w-4 p-0 text-xs">3</Badge>
              </Button>
            </TooltipTrigger>
            {isCollapsed && <TooltipContent side="right">Notifications (3)</TooltipContent>}
          </Tooltip>
          
          {isCollapsed && (
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="sm" className="text-destructive hover:bg-red-50">
                  <LogOut className="w-4 h-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">Sign Out</TooltipContent>
            </Tooltip>
          )}
        </div>
      </div>
    </motion.div>
    </TooltipProvider>
  );
}