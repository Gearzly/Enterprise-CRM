import { useState } from 'react';
import { ArrowLeft, Save, DollarSign, Calendar, TrendingUp } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Separator } from '../../components/ui/separator';

interface CreateOpportunityPageProps {
  onBack?: () => void;
  opportunityId?: string;
  isEdit?: boolean;
}

export function CreateOpportunityPage({ onBack, opportunityId, isEdit = false }: CreateOpportunityPageProps) {
  const [formData, setFormData] = useState({
    name: '',
    account: '',
    contact: '',
    amount: '',
    stage: 'prospecting',
    probability: '10',
    expectedCloseDate: '',
    leadSource: '',
    type: 'new-business',
    nextStep: '',
    description: '',
    competitorInfo: '',
    assignedTo: '',
    team: '',
    priority: 'medium',
    tags: '',
    products: '',
    campaignSource: '',
    lossReason: '',
    notes: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Opportunity data:', formData);
    if (onBack) onBack();
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const stageOptions = [
    { value: 'prospecting', label: 'Prospecting', probability: '10' },
    { value: 'qualification', label: 'Qualification', probability: '25' },
    { value: 'needs-analysis', label: 'Needs Analysis', probability: '50' },
    { value: 'proposal', label: 'Proposal/Quote', probability: '75' },
    { value: 'negotiation', label: 'Negotiation', probability: '90' },
    { value: 'closed-won', label: 'Closed Won', probability: '100' },
    { value: 'closed-lost', label: 'Closed Lost', probability: '0' }
  ];

  const handleStageChange = (stage: string) => {
    const selectedStage = stageOptions.find(s => s.value === stage);
    handleInputChange('stage', stage);
    if (selectedStage) {
      handleInputChange('probability', selectedStage.probability);
    }
  };

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
          <h1 className="text-2xl font-medium">{isEdit ? 'Edit Opportunity' : 'Create New Opportunity'}</h1>
          <p className="text-muted-foreground">
            {isEdit ? 'Update opportunity information' : 'Add a new sales opportunity to your pipeline'}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Opportunity Name *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                placeholder="e.g., Acme Corp - Software License Renewal"
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="account">Account *</Label>
                <Select value={formData.account} onValueChange={(value) => handleInputChange('account', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select account" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="acme-corp">Acme Corporation</SelectItem>
                    <SelectItem value="globex">Globex Industries</SelectItem>
                    <SelectItem value="initech">Initech Solutions</SelectItem>
                    <SelectItem value="umbrella">Umbrella Corp</SelectItem>
                    <SelectItem value="wayne-enterprises">Wayne Enterprises</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="contact">Primary Contact</Label>
                <Select value={formData.contact} onValueChange={(value) => handleInputChange('contact', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select contact" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="john-smith">John Smith</SelectItem>
                    <SelectItem value="jane-doe">Jane Doe</SelectItem>
                    <SelectItem value="mike-johnson">Mike Johnson</SelectItem>
                    <SelectItem value="sarah-wilson">Sarah Wilson</SelectItem>
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
                placeholder="Brief description of the opportunity..."
                rows={3}
              />
            </div>
          </CardContent>
        </Card>

        {/* Financial Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <DollarSign className="w-5 h-5" />
            <CardTitle>Financial Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="amount">Amount ($) *</Label>
                <Input
                  id="amount"
                  type="number"
                  value={formData.amount}
                  onChange={(e) => handleInputChange('amount', e.target.value)}
                  placeholder="0.00"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="stage">Sales Stage *</Label>
                <Select value={formData.stage} onValueChange={handleStageChange}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select stage" />
                  </SelectTrigger>
                  <SelectContent>
                    {stageOptions.map(stage => (
                      <SelectItem key={stage.value} value={stage.value}>
                        {stage.label} ({stage.probability}%)
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="probability">Probability (%)</Label>
                <Input
                  id="probability"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.probability}
                  onChange={(e) => handleInputChange('probability', e.target.value)}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="expectedCloseDate">Expected Close Date *</Label>
                <Input
                  id="expectedCloseDate"
                  type="date"
                  value={formData.expectedCloseDate}
                  onChange={(e) => handleInputChange('expectedCloseDate', e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="type">Opportunity Type</Label>
                <Select value={formData.type} onValueChange={(value) => handleInputChange('type', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="new-business">New Business</SelectItem>
                    <SelectItem value="existing-customer">Existing Customer</SelectItem>
                    <SelectItem value="renewal">Renewal</SelectItem>
                    <SelectItem value="upgrade">Upgrade</SelectItem>
                    <SelectItem value="cross-sell">Cross-sell</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Sales Process */}
        <Card>
          <CardHeader>
            <CardTitle>Sales Process</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="leadSource">Lead Source</Label>
                <Select value={formData.leadSource} onValueChange={(value) => handleInputChange('leadSource', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select source" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="website">Website</SelectItem>
                    <SelectItem value="referral">Referral</SelectItem>
                    <SelectItem value="trade-show">Trade Show</SelectItem>
                    <SelectItem value="cold-call">Cold Call</SelectItem>
                    <SelectItem value="email-campaign">Email Campaign</SelectItem>
                    <SelectItem value="social-media">Social Media</SelectItem>
                    <SelectItem value="partner">Partner</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="campaignSource">Campaign Source</Label>
                <Select value={formData.campaignSource} onValueChange={(value) => handleInputChange('campaignSource', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select campaign" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="q4-promotion">Q4 Promotion Campaign</SelectItem>
                    <SelectItem value="webinar-series">Webinar Series</SelectItem>
                    <SelectItem value="trade-show-2024">Trade Show 2024</SelectItem>
                    <SelectItem value="email-nurture">Email Nurture Campaign</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="nextStep">Next Step</Label>
              <Input
                id="nextStep"
                value={formData.nextStep}
                onChange={(e) => handleInputChange('nextStep', e.target.value)}
                placeholder="e.g., Schedule demo, Send proposal, Follow up call"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="competitorInfo">Competitor Information</Label>
              <Textarea
                id="competitorInfo"
                value={formData.competitorInfo}
                onChange={(e) => handleInputChange('competitorInfo', e.target.value)}
                placeholder="Information about competing vendors or solutions..."
                rows={3}
              />
            </div>
          </CardContent>
        </Card>

        {/* Assignment & Priority */}
        <Card>
          <CardHeader>
            <CardTitle>Assignment & Priority</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="assignedTo">Assigned To</Label>
                <Select value={formData.assignedTo} onValueChange={(value) => handleInputChange('assignedTo', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select owner" />
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
                <Label htmlFor="team">Sales Team</Label>
                <Select value={formData.team} onValueChange={(value) => handleInputChange('team', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select team" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="enterprise">Enterprise Sales</SelectItem>
                    <SelectItem value="smb">SMB Sales</SelectItem>
                    <SelectItem value="inside-sales">Inside Sales</SelectItem>
                    <SelectItem value="channel-partners">Channel Partners</SelectItem>
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
          </CardContent>
        </Card>

        {/* Products & Additional Info */}
        <Card>
          <CardHeader>
            <CardTitle>Products & Additional Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="products">Products/Services</Label>
              <Textarea
                id="products"
                value={formData.products}
                onChange={(e) => handleInputChange('products', e.target.value)}
                placeholder="List products or services included in this opportunity..."
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

            <div className="space-y-2">
              <Label htmlFor="lossReason">Loss Reason (if applicable)</Label>
              <Select value={formData.lossReason} onValueChange={(value) => handleInputChange('lossReason', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select reason" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="price">Price</SelectItem>
                  <SelectItem value="competitor">Competitor</SelectItem>
                  <SelectItem value="no-decision">No Decision</SelectItem>
                  <SelectItem value="timing">Timing</SelectItem>
                  <SelectItem value="budget">Budget</SelectItem>
                  <SelectItem value="features">Missing Features</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">Notes</Label>
              <Textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="Additional notes about this opportunity..."
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
            {isEdit ? 'Update Opportunity' : 'Create Opportunity'}
          </Button>
        </div>
      </form>
    </div>
  );
}