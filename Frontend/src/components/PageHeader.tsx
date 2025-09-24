import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from './ui/breadcrumb';
import { Calendar, Clock, ChevronRight, Search, Filter, Download, Settings, Plus, RefreshCw } from 'lucide-react';
import { motion } from 'motion/react';
import { ReactNode } from 'react';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: Array<{ label: string; href?: string }>;
  badge?: {
    text: string;
    variant?: 'default' | 'secondary' | 'destructive' | 'outline';
  };
  actions?: ReactNode;
  showDateTime?: boolean;
  gradient?: boolean;
  children?: ReactNode;
}

export function PageHeader({
  title,
  subtitle,
  breadcrumbs,
  badge,
  actions,
  showDateTime = true,
  gradient = true,
  children
}: PageHeaderProps) {
  const currentTime = new Date().toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
  
  const currentDate = new Date().toLocaleDateString('en-US', { 
    weekday: 'long',
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  return (
    <motion.div 
      className={`p-6 ${gradient ? 'bg-gradient-to-r from-background via-background to-muted/20' : 'bg-background'} border-b border-border/50`}
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Breadcrumbs */}
      {breadcrumbs && breadcrumbs.length > 0 && (
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-4"
        >
          <Breadcrumb>
            <BreadcrumbList>
              {breadcrumbs.map((crumb, index) => (
                <div key={index} className="flex items-center">
                  {index > 0 && <BreadcrumbSeparator />}
                  <BreadcrumbItem>
                    {crumb.href ? (
                      <BreadcrumbLink href={crumb.href} className="text-muted-foreground hover:text-foreground transition-colors">
                        {crumb.label}
                      </BreadcrumbLink>
                    ) : (
                      <BreadcrumbPage className="font-medium">{crumb.label}</BreadcrumbPage>
                    )}
                  </BreadcrumbItem>
                </div>
              ))}
            </BreadcrumbList>
          </Breadcrumb>
        </motion.div>
      )}

      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        {/* Title Section */}
        <motion.div 
          className="space-y-2"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center gap-3">
            <h1 className={`text-4xl font-bold ${gradient ? 'bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent' : 'text-foreground'}`}>
              {title}
            </h1>
            {badge && (
              <Badge variant={badge.variant || 'default'} className="text-sm">
                {badge.text}
              </Badge>
            )}
          </div>
          
          {subtitle && (
            <p className="text-lg text-muted-foreground max-w-2xl">
              {subtitle}
            </p>
          )}
          
          {showDateTime && (
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span>{currentDate}</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                <span>{currentTime}</span>
              </div>
            </div>
          )}
        </motion.div>

        {/* Actions Section */}
        {(actions || !actions) && (
          <motion.div 
            className="flex items-center gap-3"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            {actions || (
              <>
                <Button variant="outline" size="sm">
                  <Search className="w-4 h-4 mr-2" />
                  Search
                </Button>
                <Button variant="outline" size="sm">
                  <Filter className="w-4 h-4 mr-2" />
                  Filter
                </Button>
                <Button variant="outline" size="sm">
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </Button>
                <Button variant="outline" size="sm">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh
                </Button>
                <Button size="sm">
                  <Plus className="w-4 h-4 mr-2" />
                  Add New
                </Button>
              </>
            )}
          </motion.div>
        )}
      </div>

      {/* Additional Content */}
      {children && (
        <motion.div
          className="mt-6"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          {children}
        </motion.div>
      )}
    </motion.div>
  );
}