import React from 'react';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../../components/ui/card';
import { Link } from 'react-router-dom';

export function ForgotPasswordPage() {
  const [email, setEmail] = React.useState('');
  const [isSubmitted, setIsSubmitted] = React.useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle forgot password logic here
    console.log('Password reset request for:', email);
    setIsSubmitted(true);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">Forgot Password</CardTitle>
          <CardDescription className="text-center">
            {isSubmitted
              ? 'Check your email for a password reset link'
              : 'Enter your email to receive a password reset link'}
          </CardDescription>
        </CardHeader>
        {isSubmitted ? (
          <CardContent className="space-y-4 text-center">
            <p className="text-gray-600">
              We've sent a password reset link to <span className="font-medium">{email}</span>.
              Please check your inbox and follow the instructions to reset your password.
            </p>
            <p className="text-sm text-gray-500">
              Didn't receive the email? Check your spam folder or{' '}
              <button 
                onClick={() => setIsSubmitted(false)}
                className="font-medium text-blue-600 hover:underline"
              >
                try again
              </button>
            </p>
          </CardContent>
        ) : (
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button type="submit" className="w-full">
                Send Reset Link
              </Button>
            </CardFooter>
          </form>
        )}
        <div className="text-center pb-6">
          <Link to="/auth/login" className="text-sm font-medium text-blue-600 hover:underline">
            Back to Login
          </Link>
        </div>
      </Card>
    </div>
  );
}