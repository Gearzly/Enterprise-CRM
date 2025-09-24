import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Users, Shield, BarChart3, ArrowRight, Sparkles } from 'lucide-react';
import { motion } from 'motion/react';

interface RoleSelectorProps {
  onRoleSelect: (role: string) => void;
}

export function RoleSelector({ onRoleSelect }: RoleSelectorProps) {
  const roles = [
    {
      id: 'Sales Rep',
      title: 'Sales Representative',
      description: 'Track your personal sales performance, manage customers, and view your pipeline',
      icon: <BarChart3 className="w-10 h-10" />,
      gradient: 'from-blue-500 to-cyan-500',
      bgGradient: 'from-blue-50 to-cyan-50 dark:from-blue-950/50 to-cyan-950/50',
      borderColor: 'border-blue-200 dark:border-blue-800',
      features: ['Personal Dashboard', 'Customer Management', 'Sales Pipeline'],
      badge: 'Most Popular'
    },
    {
      id: 'Sales Manager',
      title: 'Sales Manager',
      description: 'Monitor team performance, analyze sales metrics, and manage high-value deals',
      icon: <Users className="w-10 h-10" />,
      gradient: 'from-emerald-500 to-green-500',
      bgGradient: 'from-emerald-50 to-green-50 dark:from-emerald-950/50 to-green-950/50',
      borderColor: 'border-emerald-200 dark:border-emerald-800',
      features: ['Team Analytics', 'Performance Metrics', 'Deal Management'],
      badge: 'Advanced'
    },
    {
      id: 'Admin',
      title: 'Administrator',
      description: 'Full system access, user management, and comprehensive business analytics',
      icon: <Shield className="w-10 h-10" />,
      gradient: 'from-purple-500 to-pink-500',
      bgGradient: 'from-purple-50 to-pink-50 dark:from-purple-950/50 to-pink-950/50',
      borderColor: 'border-purple-200 dark:border-purple-800',
      features: ['Full System Access', 'User Management', 'Business Analytics'],
      badge: 'Full Access'
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 flex items-center justify-center p-6">
      <div className="max-w-7xl w-full">
        <motion.div 
          className="text-center mb-12"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="w-8 h-8 text-primary" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              CRM Dashboard
            </h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Choose your role to access personalized features and insights tailored to your workflow
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {roles.map((role, index) => (
            <motion.div
              key={role.id}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -8, scale: 1.02 }}
              className="group"
            >
              <Card className={`p-8 cursor-pointer transition-all duration-300 hover:shadow-2xl bg-gradient-to-br ${role.bgGradient} ${role.borderColor} border-2 h-full relative overflow-hidden`}>
                {/* Background decoration */}
                <div className="absolute top-0 right-0 w-32 h-32 opacity-10">
                  <div className={`w-full h-full bg-gradient-to-br ${role.gradient} rounded-full transform translate-x-16 -translate-y-16`} />
                </div>
                
                <div className="relative z-10">
                  {/* Header with badge */}
                  <div className="flex items-start justify-between mb-6">
                    <motion.div 
                      className={`p-4 rounded-2xl bg-gradient-to-br ${role.gradient} text-white shadow-lg`}
                      whileHover={{ rotate: 5, scale: 1.1 }}
                      transition={{ duration: 0.2 }}
                    >
                      {role.icon}
                    </motion.div>
                    <Badge variant="secondary" className="font-medium">
                      {role.badge}
                    </Badge>
                  </div>
                  
                  {/* Content */}
                  <div className="space-y-4 mb-8">
                    <h3 className="text-2xl font-bold text-foreground">{role.title}</h3>
                    <p className="text-muted-foreground leading-relaxed">{role.description}</p>
                    
                    {/* Features list */}
                    <div className="space-y-2 pt-2">
                      {role.features.map((feature, idx) => (
                        <motion.div
                          key={feature}
                          className="flex items-center gap-2 text-sm text-muted-foreground"
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 0.3 + idx * 0.1 }}
                        >
                          <div className={`w-1.5 h-1.5 rounded-full bg-gradient-to-r ${role.gradient}`} />
                          {feature}
                        </motion.div>
                      ))}
                    </div>
                  </div>
                  
                  {/* Action button */}
                  <Button 
                    className={`w-full group-hover:scale-105 transition-all duration-300 bg-gradient-to-r ${role.gradient} hover:shadow-lg border-0 h-12`}
                    onClick={() => onRoleSelect(role.id)}
                  >
                    <span className="mr-2">Enter Dashboard</span>
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
                  </Button>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
        
        {/* Footer info */}
        <motion.div 
          className="text-center mt-12 text-sm text-muted-foreground"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <p>All roles include real-time notifications, advanced reporting, and mobile access</p>
        </motion.div>
      </div>
    </div>
  );
}