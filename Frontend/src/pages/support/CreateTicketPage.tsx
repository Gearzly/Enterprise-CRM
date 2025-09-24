import { useState } from 'react';
import { ArrowLeft, Save, AlertCircle, User, Clock } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';

interface CreateTicketPageProps {
  onBack?: () => void;
  ticketId?: string;
  isEdit?: boolean;
}

export function CreateTicketPage({ onBack, ticketId, isEdit = false }: CreateTicketPageProps) {
  const [formData, setFormData] = useState({
    subject: '',
    description: '',
    customer: '',
    customerEmail: '',
    customerPhone: '',
    priority: 'medium',
    category: '',
    subcategory: '',
    type: 'incident',
    status: 'open',
    assignedTo: '',
    team: '',
    product: '',
    version: '',
    environment: '',
    urgency: 'medium',
    impact: 'medium',
    channel: 'email',
    tags: '',
    dueDate: '',
    estimatedHours: '',
    actualHours: '',
    resolution: '',
    workaround: '',
    attachments: '',
    internalNotes: '',
    customerNotes: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Ticket data:', formData);
    if (onBack) onBack();
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const priorityOptions = [
    { value: 'low', label: 'Low', color: 'text-green-600' },
    { value: 'medium', label: 'Medium', color: 'text-yellow-600' },
    { value: 'high', label: 'High', color: 'text-orange-600' },
    { value: 'critical', label: 'Critical', color: 'text-red-600' }
  ];

  const categoryOptions = [
    'Technical Issue',
    'Bug Report',
    'Feature Request',
    'Account/Billing',
    'How-to Question',
    'Training',
    'Feedback',
    'Other'
  ];

  const typeOptions = [
    'incident',
    'service-request',
    'change-request',
    'problem',
    'inquiry'
  ];

  return (
    <div className="p-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={onBack}
          className="p-2"
        >
          <ArrowLeft className="w-4 h-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-medium">{isEdit ? 'Edit Support Ticket' : 'Create New Support Ticket'}</h1>
          <p className="text-muted-foreground">
            {isEdit ? 'Update ticket information' : 'Create a new customer support ticket'}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            <CardTitle>Ticket Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="subject">Subject *</Label>
              <Input
                id="subject"
                value={formData.subject}
                onChange={(e) => handleInputChange('subject', e.target.value)}
                placeholder="Brief description of the issue"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description *</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                placeholder="Detailed description of the issue, including steps to reproduce if applicable..."
                rows={5}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="priority">Priority *</Label>
                <Select value={formData.priority} onValueChange={(value) => handleInputChange('priority', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select priority" />
                  </SelectTrigger>
                  <SelectContent>
                    {priorityOptions.map(option => (
                      <SelectItem key={option.value} value={option.value}>
                        <span className={option.color}>{option.label}</span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="type">Type</Label>
                <Select value={formData.type} onValueChange={(value) => handleInputChange('type', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    {typeOptions.map(type => (
                      <SelectItem key={type} value={type}>
                        {type.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="channel">Channel</Label>
                <Select value={formData.channel} onValueChange={(value) => handleInputChange('channel', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select channel" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="email">Email</SelectItem>
                    <SelectItem value="phone">Phone</SelectItem>
                    <SelectItem value="chat">Live Chat</SelectItem>
                    <SelectItem value="portal">Customer Portal</SelectItem>
                    <SelectItem value="social">Social Media</SelectItem>
                    <SelectItem value="in-person">In Person</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Customer Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <User className="w-5 h-5" />
            <CardTitle>Customer Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="customer">Customer *</Label>
              <Select value={formData.customer} onValueChange={(value) => handleInputChange('customer', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select customer" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="acme-corp">Acme Corporation</SelectItem>
                  <SelectItem value="globex">Globex Industries</SelectItem>
                  <SelectItem value="initech">Initech Solutions</SelectItem>
                  <SelectItem value="umbrella">Umbrella Corp</SelectItem>
                  <SelectItem value="new-customer">+ Add New Customer</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="customerEmail">Customer Email</Label>
                <Input
                  id="customerEmail"
                  type="email"
                  value={formData.customerEmail}
                  onChange={(e) => handleInputChange('customerEmail', e.target.value)}
                  placeholder="customer@company.com"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="customerPhone">Customer Phone</Label>
                <Input
                  id="customerPhone"
                  type="tel"
                  value={formData.customerPhone}
                  onChange={(e) => handleInputChange('customerPhone', e.target.value)}
                  placeholder="+1 (555) 123-4567"
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Categorization */}
        <Card>
          <CardHeader>
            <CardTitle>Categorization</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="category">Category</Label>
                <Select value={formData.category} onValueChange={(value) => handleInputChange('category', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categoryOptions.map(category => (
                      <SelectItem key={category} value={category.toLowerCase().replace(/\s+/g, '-')}>
                        {category}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="subcategory">Subcategory</Label>
                <Input
                  id="subcategory"
                  value={formData.subcategory}
                  onChange={(e) => handleInputChange('subcategory', e.target.value)}
                  placeholder="Specific subcategory"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="product">Product/Service</Label>
                <Select value={formData.product} onValueChange={(value) => handleInputChange('product', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select product" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="crm-platform">CRM Platform</SelectItem>
                    <SelectItem value="mobile-app">Mobile App</SelectItem>
                    <SelectItem value="api">API</SelectItem>
                    <SelectItem value="integration">Integration</SelectItem>
                    <SelectItem value="training">Training</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="version">Version</Label>
                <Input
                  id="version"
                  value={formData.version}
                  onChange={(e) => handleInputChange('version', e.target.value)}
                  placeholder="e.g., v2.1.0"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="environment">Environment</Label>
                <Select value={formData.environment} onValueChange={(value) => handleInputChange('environment', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select environment" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="production">Production</SelectItem>
                    <SelectItem value="staging">Staging</SelectItem>
                    <SelectItem value="development">Development</SelectItem>
                    <SelectItem value="testing">Testing</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Impact & Urgency */}
        <Card>
          <CardHeader>
            <CardTitle>Impact & Urgency Assessment</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="urgency">Urgency</Label>
                <Select value={formData.urgency} onValueChange={(value) => handleInputChange('urgency', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select urgency" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low - Can wait weeks</SelectItem>
                    <SelectItem value="medium">Medium - Can wait days</SelectItem>
                    <SelectItem value="high">High - Can wait hours</SelectItem>
                    <SelectItem value="critical">Critical - Immediate</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="impact">Impact</Label>
                <Select value={formData.impact} onValueChange={(value) => handleInputChange('impact', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select impact" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low - Single user affected</SelectItem>
                    <SelectItem value="medium">Medium - Multiple users affected</SelectItem>
                    <SelectItem value="high">High - Department affected</SelectItem>
                    <SelectItem value="critical">Critical - Business critical</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Assignment & Timeline */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Clock className="w-5 h-5" />
            <CardTitle>Assignment & Timeline</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="assignedTo">Assigned To</Label>
                <Select value={formData.assignedTo} onValueChange={(value) => handleInputChange('assignedTo', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select agent" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="john-doe">John Doe</SelectItem>
                    <SelectItem value="jane-smith">Jane Smith</SelectItem>
                    <SelectItem value="mike-johnson">Mike Johnson</SelectItem>
                    <SelectItem value="sarah-wilson">Sarah Wilson</SelectItem>
                    <SelectItem value="auto-assign">Auto-assign</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="team">Support Team</Label>
                <Select value={formData.team} onValueChange={(value) => handleInputChange('team', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select team" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="tier-1">Tier 1 Support</SelectItem>
                    <SelectItem value="tier-2">Tier 2 Support</SelectItem>
                    <SelectItem value="technical">Technical Support</SelectItem>
                    <SelectItem value="billing">Billing Support</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="dueDate">Due Date</Label>
                <Input
                  id="dueDate"
                  type="datetime-local"
                  value={formData.dueDate}
                  onChange={(e) => handleInputChange('dueDate', e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="estimatedHours">Estimated Hours</Label>
                <Input
                  id="estimatedHours"
                  type="number"
                  step="0.5"
                  value={formData.estimatedHours}
                  onChange={(e) => handleInputChange('estimatedHours', e.target.value)}
                  placeholder="0.0"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select value={formData.status} onValueChange={(value) => handleInputChange('status', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="open">Open</SelectItem>
                    <SelectItem value="in-progress">In Progress</SelectItem>
                    <SelectItem value="pending">Pending Customer</SelectItem>
                    <SelectItem value="resolved">Resolved</SelectItem>
                    <SelectItem value="closed">Closed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Resolution & Notes */}
        <Card>
          <CardHeader>
            <CardTitle>Resolution & Notes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="workaround">Workaround (if any)</Label>
              <Textarea
                id="workaround"
                value={formData.workaround}
                onChange={(e) => handleInputChange('workaround', e.target.value)}
                placeholder="Temporary solution or workaround instructions..."
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="customerNotes">Customer Communication</Label>
              <Textarea
                id="customerNotes"
                value={formData.customerNotes}
                onChange={(e) => handleInputChange('customerNotes', e.target.value)}
                placeholder="Notes visible to customer..."
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="internalNotes">Internal Notes</Label>
              <Textarea
                id="internalNotes"
                value={formData.internalNotes}
                onChange={(e) => handleInputChange('internalNotes', e.target.value)}
                placeholder="Internal notes for support team..."
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="tags">Tags</Label>
              <Input
                id="tags"
                value={formData.tags}
                onChange={(e) => handleInputChange('tags', e.target.value)}
                placeholder="Enter tags separated by commas"
              />
            </div>
          </CardContent>
        </Card>

        {/* Form Actions */}
        <div className="flex items-center justify-end gap-4 pt-6">
          <Button type="button" variant="outline" onClick={onBack}>
            Cancel
          </Button>
          <Button type="submit" className="min-w-[120px]">
            <Save className="w-4 h-4 mr-2" />
            {isEdit ? 'Update Ticket' : 'Create Ticket'}
          </Button>
        </div>
      </form>
    </div>
  );
}