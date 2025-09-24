import { useState } from 'react';
import { ArrowLeft, Save, FileText, Eye, Code, Tag, Users } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Checkbox } from '../../components/ui/checkbox';

interface CreateKnowledgeArticlePageProps {
  onBack?: () => void;
  articleId?: string;
  isEdit?: boolean;
}

export function CreateKnowledgeArticlePage({ onBack, articleId, isEdit = false }: CreateKnowledgeArticlePageProps) {
  const [formData, setFormData] = useState({
    title: '',
    summary: '',
    category: '',
    subcategory: '',
    content: '',
    htmlContent: '',
    visibility: 'public',
    status: 'draft',
    priority: 'medium',
    difficulty: 'beginner',
    estimatedReadTime: '',
    keywords: '',
    tags: '',
    metaDescription: '',
    relatedArticles: [] as string[],
    attachments: '',
    authorNotes: '',
    reviewerNotes: '',
    featuredImage: '',
    videoUrl: '',
    isPublished: false,
    allowComments: true,
    notifyOnUpdate: false,
    expirationDate: '',
    lastReviewDate: '',
    nextReviewDate: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Knowledge article data:', formData);
    if (onBack) onBack();
  };

  const handleInputChange = (field: string, value: string | boolean | string[]) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const categories = [
    'Getting Started',
    'Account Management',
    'Features & Functionality',
    'Troubleshooting',
    'Integration',
    'API Documentation',
    'Best Practices',
    'FAQ',
    'Billing & Payments',
    'Security & Privacy'
  ];

  const visibilityOptions = [
    { value: 'public', label: 'Public - Visible to all customers' },
    { value: 'customer', label: 'Customer - Visible to logged-in customers only' },
    { value: 'internal', label: 'Internal - Visible to support team only' },
    { value: 'private', label: 'Private - Visible to author only' }
  ];

  const difficultyLevels = [
    { value: 'beginner', label: 'Beginner', color: 'text-green-600' },
    { value: 'intermediate', label: 'Intermediate', color: 'text-yellow-600' },
    { value: 'advanced', label: 'Advanced', color: 'text-red-600' }
  ];

  const estimateReadTime = (content: string) => {
    const wordsPerMinute = 200;
    const wordCount = content.split(/\s+/).length;
    const readTime = Math.ceil(wordCount / wordsPerMinute);
    setFormData(prev => ({ ...prev, estimatedReadTime: readTime.toString() }));
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
          <h1 className="text-2xl font-medium">{isEdit ? 'Edit Knowledge Article' : 'Create New Knowledge Article'}</h1>
          <p className="text-muted-foreground">
            {isEdit ? 'Update knowledge base article' : 'Create a new help article for your knowledge base'}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <FileText className="w-5 h-5" />
            <CardTitle>Article Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Article Title *</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                placeholder="How to reset your password"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="summary">Summary *</Label>
              <Textarea
                id="summary"
                value={formData.summary}
                onChange={(e) => handleInputChange('summary', e.target.value)}
                placeholder="Brief summary of what this article covers..."
                rows={3}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="category">Category *</Label>
                <Select value={formData.category} onValueChange={(value) => handleInputChange('category', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map(category => (
                      <SelectItem key={category} value={category.toLowerCase().replace(/\s+/g, '-')}>
                        {category}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="difficulty">Difficulty Level</Label>
                <Select value={formData.difficulty} onValueChange={(value) => handleInputChange('difficulty', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select difficulty" />
                  </SelectTrigger>
                  <SelectContent>
                    {difficultyLevels.map(level => (
                      <SelectItem key={level.value} value={level.value}>
                        <span className={level.color}>{level.label}</span>
                      </SelectItem>
                    ))}
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

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="subcategory">Subcategory</Label>
                <Input
                  id="subcategory"
                  value={formData.subcategory}
                  onChange={(e) => handleInputChange('subcategory', e.target.value)}
                  placeholder="Password Recovery"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="estimatedReadTime">Estimated Read Time (minutes)</Label>
                <Input
                  id="estimatedReadTime"
                  type="number"
                  min="1"
                  value={formData.estimatedReadTime}
                  onChange={(e) => handleInputChange('estimatedReadTime', e.target.value)}
                  placeholder="Auto-calculated"
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Content */}
        <Card>
          <CardHeader>
            <CardTitle>Article Content</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="editor" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="editor" className="flex items-center gap-2">
                  <Eye className="w-4 h-4" />
                  Rich Editor
                </TabsTrigger>
                <TabsTrigger value="html" className="flex items-center gap-2">
                  <Code className="w-4 h-4" />
                  HTML Source
                </TabsTrigger>
              </TabsList>

              <TabsContent value="editor" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="content">Article Content *</Label>
                  <Textarea
                    id="content"
                    value={formData.content}
                    onChange={(e) => {
                      handleInputChange('content', e.target.value);
                      estimateReadTime(e.target.value);
                    }}
                    placeholder="Write your article content here..."
                    rows={20}
                    required
                  />
                  <p className="text-sm text-muted-foreground">
                    Word count: {formData.content.split(/\s+/).filter(word => word.length > 0).length}
                  </p>
                </div>
              </TabsContent>

              <TabsContent value="html" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="htmlContent">HTML Content</Label>
                  <Textarea
                    id="htmlContent"
                    value={formData.htmlContent}
                    onChange={(e) => handleInputChange('htmlContent', e.target.value)}
                    placeholder="<p>HTML content here...</p>"
                    rows={20}
                    className="font-mono text-sm"
                  />
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        {/* Media & Attachments */}
        <Card>
          <CardHeader>
            <CardTitle>Media & Attachments</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="featuredImage">Featured Image URL</Label>
              <Input
                id="featuredImage"
                type="url"
                value={formData.featuredImage}
                onChange={(e) => handleInputChange('featuredImage', e.target.value)}
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="videoUrl">Video URL</Label>
              <Input
                id="videoUrl"
                type="url"
                value={formData.videoUrl}
                onChange={(e) => handleInputChange('videoUrl', e.target.value)}
                placeholder="https://youtube.com/watch?v=..."
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="attachments">Attachments</Label>
              <Textarea
                id="attachments"
                value={formData.attachments}
                onChange={(e) => handleInputChange('attachments', e.target.value)}
                placeholder="List of attachment URLs, one per line"
                rows={3}
              />
            </div>
          </CardContent>
        </Card>

        {/* Visibility & Publishing */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Users className="w-5 h-5" />
            <CardTitle>Visibility & Publishing</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="visibility">Visibility</Label>
                <Select value={formData.visibility} onValueChange={(value) => handleInputChange('visibility', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select visibility" />
                  </SelectTrigger>
                  <SelectContent>
                    {visibilityOptions.map(option => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
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
                    <SelectItem value="review">Under Review</SelectItem>
                    <SelectItem value="approved">Approved</SelectItem>
                    <SelectItem value="published">Published</SelectItem>
                    <SelectItem value="archived">Archived</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="lastReviewDate">Last Review Date</Label>
                <Input
                  id="lastReviewDate"
                  type="date"
                  value={formData.lastReviewDate}
                  onChange={(e) => handleInputChange('lastReviewDate', e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="nextReviewDate">Next Review Date</Label>
                <Input
                  id="nextReviewDate"
                  type="date"
                  value={formData.nextReviewDate}
                  onChange={(e) => handleInputChange('nextReviewDate', e.target.value)}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="expirationDate">Expiration Date (optional)</Label>
              <Input
                id="expirationDate"
                type="date"
                value={formData.expirationDate}
                onChange={(e) => handleInputChange('expirationDate', e.target.value)}
              />
            </div>

            <div className="flex gap-6">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="isPublished"
                  checked={formData.isPublished}
                  onCheckedChange={(checked) => handleInputChange('isPublished', checked as boolean)}
                />
                <Label htmlFor="isPublished">Publish immediately</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="allowComments"
                  checked={formData.allowComments}
                  onCheckedChange={(checked) => handleInputChange('allowComments', checked as boolean)}
                />
                <Label htmlFor="allowComments">Allow comments</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="notifyOnUpdate"
                  checked={formData.notifyOnUpdate}
                  onCheckedChange={(checked) => handleInputChange('notifyOnUpdate', checked as boolean)}
                />
                <Label htmlFor="notifyOnUpdate">Notify subscribers on update</Label>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* SEO & Metadata */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Tag className="w-5 h-5" />
            <CardTitle>SEO & Metadata</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="metaDescription">Meta Description</Label>
              <Textarea
                id="metaDescription"
                value={formData.metaDescription}
                onChange={(e) => handleInputChange('metaDescription', e.target.value)}
                placeholder="Brief description for search engines..."
                rows={2}
                maxLength={160}
              />
              <p className="text-sm text-muted-foreground">
                {formData.metaDescription.length}/160 characters
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="keywords">Keywords</Label>
              <Input
                id="keywords"
                value={formData.keywords}
                onChange={(e) => handleInputChange('keywords', e.target.value)}
                placeholder="keyword1, keyword2, keyword3"
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

        {/* Internal Notes */}
        <Card>
          <CardHeader>
            <CardTitle>Internal Notes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="authorNotes">Author Notes</Label>
              <Textarea
                id="authorNotes"
                value={formData.authorNotes}
                onChange={(e) => handleInputChange('authorNotes', e.target.value)}
                placeholder="Notes for the author..."
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="reviewerNotes">Reviewer Notes</Label>
              <Textarea
                id="reviewerNotes"
                value={formData.reviewerNotes}
                onChange={(e) => handleInputChange('reviewerNotes', e.target.value)}
                placeholder="Notes for reviewers..."
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
            {isEdit ? 'Update Article' : 'Create Article'}
          </Button>
        </div>
      </form>
    </div>
  );
}