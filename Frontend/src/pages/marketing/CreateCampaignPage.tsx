import { useState } from 'react';
import { ArrowLeft, Save, Megaphone, Calendar, Target, DollarSign } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Checkbox } from '../../components/ui/checkbox';

interface CreateCampaignPageProps {
  onBack?: () => void;
  campaignId?: string;
  isEdit?: boolean;
}

export function CreateCampaignPage({ onBack, campaignId, isEdit = false }: CreateCampaignPageProps) {
  const [formData, setFormData] = useState({
    name: '',
    type: 'email',
    status: 'draft',
    startDate: '',
    endDate: '',
    budget: '',
    expectedRevenue: '',
    description: '',
    objective: '',
    targetAudience: '',
    channels: [] as string[],
    assignedTo: '',
    team: '',
    priority: 'medium',
    tags: '',
    landingPageUrl: '',
    utmSource: '',
    utmMedium: '',
    utmCampaign: '',
    notes: '',
    isRecurring: false,
    frequency: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Campaign data:', formData);
    if (onBack) onBack();
  };

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleChannelChange = (channel: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      channels: checked 
        ? [...prev.channels, channel]
        : prev.channels.filter(c => c !== channel)
    }));
  };

  const campaignTypes = [
    'email',
    'social-media',
    'content-marketing',
    'paid-advertising',
    'webinar',
    'trade-show',
    'direct-mail',
    'telemarketing',
    'partner',
    'other'
  ];

  const marketingChannels = [
    'Email',
    'Social Media',
    'Google Ads',
    'Facebook Ads',
    'LinkedIn Ads',
    'Content Marketing',
    'SEO',
    'Webinars',
    'Trade Shows',
    'Direct Mail',
    'Print Advertising',
    'Radio',
    'TV',
    'Outdoor'
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
          <h1 className="text-2xl font-medium">{isEdit ? 'Edit Campaign' : 'Create New Campaign'}</h1>
          <p className="text-muted-foreground">
            {isEdit ? 'Update campaign information' : 'Create a new marketing campaign'}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Megaphone className="w-5 h-5" />
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Campaign Name *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                placeholder="e.g., Q1 Product Launch Campaign"
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="type">Campaign Type *</Label>
                <Select value={formData.type} onValueChange={(value) => handleInputChange('type', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    {campaignTypes.map(type => (
                      <SelectItem key={type} value={type}>
                        {type.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      </SelectItem>
                    ))}
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
                    <SelectItem value="planned">Planned</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="paused">Paused</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                    <SelectItem value="cancelled">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="priority">Priority</Label>
                <Select value={formData.priority} onValueChange={(value) => handleInputChange('priority', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select priority" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="urgent">Urgent</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                placeholder="Brief description of the campaign..."
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="objective">Campaign Objective</Label>
              <Textarea
                id="objective"
                value={formData.objective}
                onChange={(e) => handleInputChange('objective', e.target.value)}
                placeholder="What are the main goals and objectives of this campaign?"
                rows={2}
              />
            </div>
          </CardContent>
        </Card>

        {/* Timeline & Budget */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Calendar className="w-5 h-5" />
            <CardTitle>Timeline & Budget</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="startDate">Start Date *</Label>
                <Input
                  id="startDate"
                  type="date"
                  value={formData.startDate}
                  onChange={(e) => handleInputChange('startDate', e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="endDate">End Date</Label>
                <Input
                  id="endDate"
                  type="date"
                  value={formData.endDate}
                  onChange={(e) => handleInputChange('endDate', e.target.value)}
                />
              </div>
            </div>

            <div className="flex items-center space-x-2 mb-4">
              <Checkbox
                id="isRecurring"
                checked={formData.isRecurring}
                onCheckedChange={(checked) => handleInputChange('isRecurring', checked as boolean)}
              />
              <Label htmlFor="isRecurring">Recurring Campaign</Label>
            </div>

            {formData.isRecurring && (
              <div className="space-y-2">
                <Label htmlFor="frequency">Frequency</Label>
                <Select value={formData.frequency} onValueChange={(value) => handleInputChange('frequency', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select frequency" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="weekly">Weekly</SelectItem>
                    <SelectItem value="monthly">Monthly</SelectItem>
                    <SelectItem value="quarterly">Quarterly</SelectItem>
                    <SelectItem value="annually">Annually</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="budget">Budget ($)</Label>
                <Input
                  id="budget"
                  type="number"
                  value={formData.budget}
                  onChange={(e) => handleInputChange('budget', e.target.value)}
                  placeholder="0.00"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="expectedRevenue">Expected Revenue ($)</Label>
                <Input
                  id="expectedRevenue"
                  type="number"
                  value={formData.expectedRevenue}
                  onChange={(e) => handleInputChange('expectedRevenue', e.target.value)}
                  placeholder="0.00"
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Target Audience & Channels */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Target className="w-5 h-5" />
            <CardTitle>Target Audience & Channels</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="targetAudience">Target Audience</Label>
              <Textarea
                id="targetAudience"
                value={formData.targetAudience}
                onChange={(e) => handleInputChange('targetAudience', e.target.value)}
                placeholder="Describe your target audience, demographics, interests, etc..."
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label>Marketing Channels</Label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {marketingChannels.map(channel => (
                  <div key={channel} className="flex items-center space-x-2">
                    <Checkbox
                      id={channel}
                      checked={formData.channels.includes(channel)}
                      onCheckedChange={(checked) => handleChannelChange(channel, checked as boolean)}
                    />
                    <Label htmlFor={channel} className="text-sm">{channel}</Label>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Assignment & Team */}
        <Card>
          <CardHeader>
            <CardTitle>Assignment & Team</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="assignedTo">Campaign Manager</Label>
                <Select value={formData.assignedTo} onValueChange={(value) => handleInputChange('assignedTo', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select manager" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="john-doe">John Doe</SelectItem>
                    <SelectItem value="jane-smith">Jane Smith</SelectItem>
                    <SelectItem value="mike-johnson">Mike Johnson</SelectItem>
                    <SelectItem value="sarah-wilson">Sarah Wilson</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="team">Marketing Team</Label>
                <Select value={formData.team} onValueChange={(value) => handleInputChange('team', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select team" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="digital-marketing">Digital Marketing</SelectItem>
                    <SelectItem value="content-marketing">Content Marketing</SelectItem>
                    <SelectItem value="event-marketing">Event Marketing</SelectItem>
                    <SelectItem value="product-marketing">Product Marketing</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tracking & Analytics */}
        <Card>
          <CardHeader>
            <CardTitle>Tracking & Analytics</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="landingPageUrl">Landing Page URL</Label>
              <Input
                id="landingPageUrl"
                type="url"
                value={formData.landingPageUrl}
                onChange={(e) => handleInputChange('landingPageUrl', e.target.value)}
                placeholder="https://"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="utmSource">UTM Source</Label>
                <Input
                  id="utmSource"
                  value={formData.utmSource}
                  onChange={(e) => handleInputChange('utmSource', e.target.value)}
                  placeholder="e.g., google, facebook, newsletter"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="utmMedium">UTM Medium</Label>
                <Input
                  id="utmMedium"
                  value={formData.utmMedium}
                  onChange={(e) => handleInputChange('utmMedium', e.target.value)}
                  placeholder="e.g., email, social, cpc"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="utmCampaign">UTM Campaign</Label>
                <Input
                  id="utmCampaign"
                  value={formData.utmCampaign}
                  onChange={(e) => handleInputChange('utmCampaign', e.target.value)}
                  placeholder="e.g., spring_sale, product_launch"
                />
              </div>
            </div>
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
              <Label htmlFor="notes">Notes</Label>
              <Textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="Additional notes about this campaign..."
                rows={4}
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
            {isEdit ? 'Update Campaign' : 'Create Campaign'}
          </Button>
        </div>
      </form>
    </div>
  );
}