import { useState } from 'react';
import { ArrowLeft, Save, Mail, Eye, Code, Image } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Checkbox } from '../../components/ui/checkbox';

interface CreateEmailTemplatePageProps {
  onBack?: () => void;
  templateId?: string;
  isEdit?: boolean;
}

export function CreateEmailTemplatePage({ onBack, templateId, isEdit = false }: CreateEmailTemplatePageProps) {
  const [formData, setFormData] = useState({
    name: '',
    subject: '',
    preheader: '',
    category: 'marketing',
    type: 'promotional',
    fromName: '',
    fromEmail: '',
    replyTo: '',
    htmlContent: '',
    textContent: '',
    tags: '',
    status: 'draft',
    isActive: true,
    trackOpens: true,
    trackClicks: true,
    notes: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Email template data:', formData);
    if (onBack) onBack();
  };

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const insertVariable = (variable: string) => {
    const textarea = document.getElementById('htmlContent') as HTMLTextAreaElement;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      const before = text.substring(0, start);
      const after = text.substring(end, text.length);
      const newText = before + `{{${variable}}}` + after;
      setFormData(prev => ({ ...prev, htmlContent: newText }));
    }
  };

  const predefinedVariables = [
    'first_name',
    'last_name',
    'email',
    'company',
    'position',
    'phone',
    'city',
    'state',
    'country'
  ];

  const emailTemplates = {
    welcome: {
      subject: 'Welcome to {{company_name}}!',
      html: `<h1>Welcome {{first_name}}!</h1>
<p>Thank you for joining {{company_name}}. We're excited to have you on board.</p>
<p>Get started by:</p>
<ul>
  <li>Completing your profile</li>
  <li>Exploring our features</li>
  <li>Connecting with our team</li>
</ul>
<p>Best regards,<br>The {{company_name}} Team</p>`
    },
    promotional: {
      subject: 'Special Offer Just for You!',
      html: `<h1>Hi {{first_name}},</h1>
<p>We have an exclusive offer just for you!</p>
<div style="background: #f5f5f5; padding: 20px; margin: 20px 0; text-align: center;">
  <h2>Get 20% Off Your Next Purchase</h2>
  <p>Use code: SAVE20</p>
</div>
<p>This offer expires soon, so don't wait!</p>
<p>Shop now and save!</p>`
    },
    newsletter: {
      subject: 'Your Monthly Newsletter - {{month}} Edition',
      html: `<h1>{{company_name}} Newsletter</h1>
<h2>What's New This Month</h2>
<p>Here are the latest updates and insights:</p>
<ul>
  <li>Feature update 1</li>
  <li>Industry news</li>
  <li>Customer spotlight</li>
</ul>
<p>Thank you for being a valued subscriber!</p>`
    }
  };

  const loadTemplate = (templateKey: string) => {
    const template = emailTemplates[templateKey as keyof typeof emailTemplates];
    if (template) {
      setFormData(prev => ({
        ...prev,
        subject: template.subject,
        htmlContent: template.html
      }));
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
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
          <h1 className="text-2xl font-medium">{isEdit ? 'Edit Email Template' : 'Create New Email Template'}</h1>
          <p className="text-muted-foreground">
            {isEdit ? 'Update email template' : 'Create a reusable email template for campaigns'}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Mail className="w-5 h-5" />
            <CardTitle>Template Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Template Name *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="e.g., Welcome Email Template"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="category">Category</Label>
                <Select value={formData.category} onValueChange={(value) => handleInputChange('category', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="marketing">Marketing</SelectItem>
                    <SelectItem value="transactional">Transactional</SelectItem>
                    <SelectItem value="newsletter">Newsletter</SelectItem>
                    <SelectItem value="notification">Notification</SelectItem>
                    <SelectItem value="welcome">Welcome Series</SelectItem>
                    <SelectItem value="follow-up">Follow-up</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="type">Email Type</Label>
                <Select value={formData.type} onValueChange={(value) => handleInputChange('type', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="promotional">Promotional</SelectItem>
                    <SelectItem value="informational">Informational</SelectItem>
                    <SelectItem value="welcome">Welcome</SelectItem>
                    <SelectItem value="reminder">Reminder</SelectItem>
                    <SelectItem value="announcement">Announcement</SelectItem>
                    <SelectItem value="survey">Survey</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select value={formData.status} onValueChange={(value) => handleInputChange('status', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="archived">Archived</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Quick Templates</Label>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => loadTemplate('welcome')}
                >
                  Welcome Email
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => loadTemplate('promotional')}
                >
                  Promotional
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => loadTemplate('newsletter')}
                >
                  Newsletter
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Email Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Email Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="fromName">From Name</Label>
                <Input
                  id="fromName"
                  value={formData.fromName}
                  onChange={(e) => handleInputChange('fromName', e.target.value)}
                  placeholder="Your Company Name"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="fromEmail">From Email</Label>
                <Input
                  id="fromEmail"
                  type="email"
                  value={formData.fromEmail}
                  onChange={(e) => handleInputChange('fromEmail', e.target.value)}
                  placeholder="noreply@yourcompany.com"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="replyTo">Reply-To Email</Label>
              <Input
                id="replyTo"
                type="email"
                value={formData.replyTo}
                onChange={(e) => handleInputChange('replyTo', e.target.value)}
                placeholder="support@yourcompany.com"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="subject">Subject Line *</Label>
              <Input
                id="subject"
                value={formData.subject}
                onChange={(e) => handleInputChange('subject', e.target.value)}
                placeholder="Enter email subject line..."
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="preheader">Preheader Text</Label>
              <Input
                id="preheader"
                value={formData.preheader}
                onChange={(e) => handleInputChange('preheader', e.target.value)}
                placeholder="Preview text that appears after the subject line"
                maxLength={100}
              />
              <p className="text-sm text-muted-foreground">
                {formData.preheader.length}/100 characters
              </p>
            </div>

            <div className="flex gap-6">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="isActive"
                  checked={formData.isActive}
                  onCheckedChange={(checked) => handleInputChange('isActive', checked as boolean)}
                />
                <Label htmlFor="isActive">Active Template</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="trackOpens"
                  checked={formData.trackOpens}
                  onCheckedChange={(checked) => handleInputChange('trackOpens', checked as boolean)}
                />
                <Label htmlFor="trackOpens">Track Opens</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="trackClicks"
                  checked={formData.trackClicks}
                  onCheckedChange={(checked) => handleInputChange('trackClicks', checked as boolean)}
                />
                <Label htmlFor="trackClicks">Track Clicks</Label>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Email Content */}
        <Card>
          <CardHeader>
            <CardTitle>Email Content</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="visual" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="visual" className="flex items-center gap-2">
                  <Eye className="w-4 h-4" />
                  Visual Editor
                </TabsTrigger>
                <TabsTrigger value="html" className="flex items-center gap-2">
                  <Code className="w-4 h-4" />
                  HTML
                </TabsTrigger>
                <TabsTrigger value="text" className="flex items-center gap-2">
                  Text Version
                </TabsTrigger>
              </TabsList>

              <TabsContent value="visual" className="space-y-4">
                <div className="border rounded-lg p-4 min-h-[400px] bg-white">
                  <div className="text-sm text-muted-foreground mb-4">
                    Visual editor would be implemented here with a rich text editor like TinyMCE or similar.
                  </div>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="htmlContent">HTML Content *</Label>
                      <Textarea
                        id="htmlContent"
                        value={formData.htmlContent}
                        onChange={(e) => handleInputChange('htmlContent', e.target.value)}
                        placeholder="Enter your email content here..."
                        rows={15}
                        className="font-mono text-sm"
                        required
                      />
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="html" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="htmlContent">HTML Content *</Label>
                  <Textarea
                    id="htmlContent"
                    value={formData.htmlContent}
                    onChange={(e) => handleInputChange('htmlContent', e.target.value)}
                    placeholder="Enter HTML content..."
                    rows={20}
                    className="font-mono text-sm"
                    required
                  />
                </div>
              </TabsContent>

              <TabsContent value="text" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="textContent">Plain Text Content</Label>
                  <Textarea
                    id="textContent"
                    value={formData.textContent}
                    onChange={(e) => handleInputChange('textContent', e.target.value)}
                    placeholder="Enter plain text version of your email..."
                    rows={15}
                  />
                </div>
              </TabsContent>
            </Tabs>

            {/* Variable Insertion */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Personalization Variables</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Click a variable to insert it at the cursor position in your content.
                </p>
                <div className="grid grid-cols-3 md:grid-cols-5 gap-2">
                  {predefinedVariables.map(variable => (
                    <Button
                      key={variable}
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => insertVariable(variable)}
                      className="text-xs"
                    >
                      {variable}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </CardContent>
        </Card>

        {/* Additional Information */}
        <Card>
          <CardHeader>
            <CardTitle>Additional Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="tags">Tags</Label>
              <Input
                id="tags"
                value={formData.tags}
                onChange={(e) => handleInputChange('tags', e.target.value)}
                placeholder="Enter tags separated by commas"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">Internal Notes</Label>
              <Textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="Internal notes about this template..."
                rows={3}
              />
            </div>
          </CardContent>
        </Card>

        {/* Form Actions */}
        <div className="flex items-center justify-end gap-4 pt-6">
          <Button type="button" variant="outline" onClick={onBack}>
            Cancel
          </Button>
          <Button type="button" variant="secondary">
            <Eye className="w-4 h-4 mr-2" />
            Preview
          </Button>
          <Button type="submit" className="min-w-[120px]">
            <Save className="w-4 h-4 mr-2" />
            {isEdit ? 'Update Template' : 'Create Template'}
          </Button>
        </div>
      </form>
    </div>
  );
}