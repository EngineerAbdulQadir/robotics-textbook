import React, { useState } from 'react';
import styles from './AuthModal.module.css';
import { useAuth, User } from '@site/src/contexts/AuthContext';
import { Lock, UserPlus, User as UserIcon, Mail, Key, Briefcase, Code, Target, LogOut, CheckCircle, XCircle, Info, Eye, EyeOff, ArrowRight, Sparkles, Shield } from 'lucide-react';

interface AuthModalProps {
  isOpen?: boolean;
  onClose?: () => void;
  onAuthSuccess?: (user: User) => void;
}

// Backend API URL - points to Render deployment
const getApiUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:3001';
  return window.location.hostname === 'localhost'
    ? 'http://localhost:3001'
    : 'https://rag-chatbot-backend-production-5f64.up.railway.app';
};

export default function AuthModal({ isOpen: propIsOpen, onClose: propOnClose, onAuthSuccess }: AuthModalProps) {
  const { user, setUser, isAuthModalOpen, closeAuthModal, checkSession } = useAuth();

  // Support both controlled (props) and context-based usage
  const isOpen = propIsOpen !== undefined ? propIsOpen : isAuthModalOpen;
  const onClose = propOnClose || closeAuthModal;

  const [mode, setMode] = useState<'signin' | 'signup'>('signin');
  const [signupStep, setSignupStep] = useState<1 | 2>(1); // Step 1: Basic info, Step 2: Background
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error' | 'info'>('info');
  const [showPassword, setShowPassword] = useState(false);

  // Form states - Basic Info
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  // Form states - Background Info
  const [softwareExperience, setSoftwareExperience] = useState<string>('');
  const [hardwareExperience, setHardwareExperience] = useState<string>('');
  const [programmingLanguages, setProgrammingLanguages] = useState<string[]>([]);
  const [roboticsBackground, setRoboticsBackground] = useState<string>('');
  const [learningGoals, setLearningGoals] = useState<string>('');

  const API_URL = getApiUrl();

  const showMessage = (msg: string, type: 'success' | 'error' | 'info') => {
    setMessage(msg);
    setMessageType(type);
  };

  const handleNextStep = (e: React.FormEvent) => {
    e.preventDefault();
    if (signupStep === 1) {
      // Validate basic info before moving to step 2
      if (!email || !password || !name) {
        showMessage('Please fill in all fields', 'error');
        return;
      }
      setSignupStep(2);
      setMessage('');
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      console.log('Attempting sign up to:', `${API_URL}/api/auth/sign-up/email`);
      const response = await fetch(`${API_URL}/api/auth/sign-up/email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ 
          email, 
          password, 
          name,
          // Background information
          softwareExperience,
          hardwareExperience,
          programmingLanguages,
          roboticsBackground,
          learningGoals
        }),
      });

      console.log('Sign up response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Sign up error:', errorText);
        throw new Error(errorText || 'Sign up failed');
      }

      let data;
      try {
        const responseText = await response.text();
        console.log('Response text:', responseText.substring(0, 500)); // Log first 500 chars
        data = JSON.parse(responseText);
      } catch (parseError) {
        console.error('JSON parse error:', parseError);
        // If JSON parsing fails but response was 200, consider it a success
        data = { user: { email } };
      }

      if (response.ok) {
        showMessage('Account created! Setting up your profile...', 'success');
        setUser(data.user);
        
        // Create user profile with background information
        try {
          await fetch(`${API_URL}/api/users/profile/init`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
              softwareExperience,
              hardwareExperience,
              programmingLanguages,
              roboticsBackground,
              learningGoals,
            }),
          });
          console.log('✅ Profile created successfully');
        } catch (profileError) {
          console.error('Profile creation failed:', profileError);
          // Don't fail the sign-up if profile creation fails
        }
        
        setTimeout(() => {
          onAuthSuccess?.(data.user);
          onClose();
          setSignupStep(1); // Reset for next time
        }, 1000);
      } else {
        showMessage(`${data.message || 'Sign up failed'}`, 'error');
      }
    } catch (error) {
      showMessage(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      console.log('Attempting sign in to:', `${API_URL}/api/auth/sign-in/email`);
      const response = await fetch(`${API_URL}/api/auth/sign-in/email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password }),
      });

      console.log('Sign in response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Sign in error:', errorText);
        throw new Error(errorText || 'Sign in failed');
      }

      const data = await response.json();

      if (response.ok) {
        showMessage('Signed in successfully!', 'success');
        setUser(data.user);
        setTimeout(() => {
          onAuthSuccess?.(data.user);
          onClose();
        }, 1000);
      } else {
        showMessage(`${data.message || 'Sign in failed'}`, 'error');
      }
    } catch (error) {
      showMessage(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSignOut = async () => {
    try {
      // Call custom sign-out endpoint that clears HTTP-only cookies
      await fetch(`${API_URL}/api/auth/sign-out-clear`, {
        method: 'POST',
        credentials: 'include',
      });
      
      // Clear user state
      setUser(null);
      showMessage('Signed out successfully', 'success');
      
      // Close modal and reload page to clear all state
      setTimeout(() => {
        onClose();
        window.location.reload();
      }, 500);
    } catch (error) {
      console.error('Sign out error:', error);
      setUser(null);
      showMessage('Signed out', 'success');
      setTimeout(() => {
        onClose();
        window.location.reload();
      }, 500);
    }
  };

  if (!isOpen) return null;

  return (
    <div className={styles.modal}>
      <div className={styles.overlay} onClick={onClose} />
      <div className={styles.content}>
        <button className={styles.closeBtn} onClick={onClose}>×</button>

        {user ? (
          // Logged In View - Modern Design
          <div className={styles.container}>
            <div className={styles.profileHeader}>
              <div className={styles.avatarCircle}>
                <UserIcon size={32} />
              </div>
              <h2 className={styles.welcomeTitle}>Welcome back!</h2>
              <p className={styles.userName}>{user.name || user.email.split('@')[0]}</p>
            </div>

            <div className={styles.userInfoCard}>
              <div className={styles.infoRow}>
                <Mail size={18} className={styles.infoIcon} />
                <div className={styles.infoContent}>
                  <span className={styles.infoLabel}>Email</span>
                  <span className={styles.infoValue}>{user.email}</span>
                </div>
              </div>
              <div className={styles.infoRow}>
                <Shield size={18} className={styles.infoIcon} />
                <div className={styles.infoContent}>
                  <span className={styles.infoLabel}>Account Status</span>
                  <span className={styles.statusBadge}>
                    <CheckCircle size={14} />
                    Active
                  </span>
                </div>
              </div>
            </div>

            <div className={styles.featuresList}>
              <div className={styles.featureItem}>
                <CheckCircle size={16} className={styles.featureIcon} />
                <span>Personalized learning experience</span>
              </div>
              <div className={styles.featureItem}>
                <CheckCircle size={16} className={styles.featureIcon} />
                <span>Track your progress</span>
              </div>
              <div className={styles.featureItem}>
                <CheckCircle size={16} className={styles.featureIcon} />
                <span>Save your favorite lessons</span>
              </div>
            </div>

            <button
              className={styles.signOutBtn}
              onClick={handleSignOut}
            >
              <LogOut size={18} />
              Sign Out
            </button>
          </div>
        ) : (
          // Sign In / Sign Up View
          <div className={styles.container}>
            {message && (
              <div className={`${styles.message} ${styles[messageType]}`}>
                {message}
              </div>
            )}

            {mode === 'signin' ? (
              // Sign In Form - Modern Design
              <>
                <div className={styles.formHeader}>
                  <div className={styles.iconWrapper}>
                    <Lock size={24} />
                  </div>
                  <h3 className={styles.formTitle}>Welcome Back</h3>
                  <p className={styles.formSubtitle}>Sign in to continue your learning journey</p>
                </div>

                <form onSubmit={handleSignIn}>
                  <div className={styles.formGroup}>
                    <label>Email Address</label>
                    <div className={styles.inputWrapper}>
                      <Mail size={18} className={styles.inputIcon} />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="you@example.com"
                        className={styles.inputWithIcon}
                        required
                      />
                    </div>
                  </div>

                  <div className={styles.formGroup}>
                    <label>Password</label>
                    <div className={styles.inputWrapper}>
                      <Key size={18} className={styles.inputIcon} />
                      <input
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        className={styles.inputWithIcon}
                        required
                      />
                      <button
                        type="button"
                        className={styles.passwordToggle}
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  </div>

                  <button type="submit" className={styles.submitBtn} disabled={loading}>
                    {loading ? (
                      <>
                        <div className={styles.spinner}></div>
                        Signing in...
                      </>
                    ) : (
                      <>
                        Sign In
                        <ArrowRight size={18} />
                      </>
                    )}
                  </button>
                </form>
              </>
            ) : signupStep === 1 ? (
              // Sign Up Step 1: Basic Information - Modern Design
              <>
                <div className={styles.formHeader}>
                  <div className={styles.iconWrapper}>
                    <Sparkles size={24} />
                  </div>
                  <h3 className={styles.formTitle}>Create Your Account</h3>
                  <p className={styles.formSubtitle}>Let's get started with the basics</p>
                </div>

                <div className={styles.stepIndicator}>
                  <div className={`${styles.stepDot} ${styles.active}`}>1</div>
                  <div className={styles.stepLine}></div>
                  <div className={styles.stepDot}>2</div>
                </div>

                <form onSubmit={handleNextStep}>
                  <div className={styles.formGroup}>
                    <label>Full Name</label>
                    <div className={styles.inputWrapper}>
                      <UserIcon size={18} className={styles.inputIcon} />
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Enter your full name"
                        className={styles.inputWithIcon}
                        required
                      />
                    </div>
                  </div>

                  <div className={styles.formGroup}>
                    <label>Email Address</label>
                    <div className={styles.inputWrapper}>
                      <Mail size={18} className={styles.inputIcon} />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="you@example.com"
                        className={styles.inputWithIcon}
                        required
                      />
                    </div>
                  </div>

                  <div className={styles.formGroup}>
                    <label>Password</label>
                    <div className={styles.inputWrapper}>
                      <Key size={18} className={styles.inputIcon} />
                      <input
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Create a strong password (min 8 characters)"
                        className={styles.inputWithIcon}
                        required
                      />
                      <button
                        type="button"
                        className={styles.passwordToggle}
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                    <p className={styles.passwordHint}>Use at least 8 characters with a mix of letters and numbers</p>
                  </div>

                  <button type="submit" className={styles.submitBtn}>
                    Continue to Background Info
                    <ArrowRight size={18} />
                  </button>
                </form>
              </>
            ) : (
              // Sign Up Step 2: Background Information - Modern Design
              <>
                <div className={styles.formHeader}>
                  <div className={styles.iconWrapper}>
                    <Target size={24} />
                  </div>
                  <h3 className={styles.formTitle}>Tell Us About Yourself</h3>
                  <p className={styles.formSubtitle}>Help us personalize your learning experience</p>
                </div>

                <div className={styles.stepIndicator}>
                  <div className={`${styles.stepDot} ${styles.completed}`}>
                    <CheckCircle size={14} />
                  </div>
                  <div className={`${styles.stepLine} ${styles.completed}`}></div>
                  <div className={`${styles.stepDot} ${styles.active}`}>2</div>
                </div>

                <form onSubmit={handleSignUp}>
                  <div className={styles.formGroup}>
                    <label>
                      <Code size={16} className={styles.labelIcon} />
                      Software Development Experience
                    </label>
                    <select
                      value={softwareExperience}
                      onChange={(e) => setSoftwareExperience(e.target.value)}
                      className={styles.selectInput}
                      required
                    >
                      <option value="">Select your experience level</option>
                      <option value="none">No experience</option>
                      <option value="beginner">Beginner (&lt; 1 year)</option>
                      <option value="intermediate">Intermediate (1-3 years)</option>
                      <option value="advanced">Advanced (3+ years)</option>
                      <option value="professional">Professional (5+ years)</option>
                    </select>
                  </div>

                  <div className={styles.formGroup}>
                    <label>
                      <Briefcase size={16} className={styles.labelIcon} />
                      Hardware/Robotics Background
                    </label>
                    <select
                      value={hardwareExperience}
                      onChange={(e) => setHardwareExperience(e.target.value)}
                      className={styles.selectInput}
                      required
                    >
                      <option value="">Select your background</option>
                      <option value="none">No experience</option>
                      <option value="hobbyist">Hobbyist/DIY projects</option>
                      <option value="academic">Academic/Research</option>
                      <option value="professional">Professional/Industry</option>
                    </select>
                  </div>

                  <div className={styles.formGroup}>
                    <label>Programming Languages</label>
                    <p className={styles.fieldDescription}>Select all that apply</p>
                    <div className={styles.checkboxGrid}>
                      {['Python', 'C++', 'JavaScript', 'Java', 'MATLAB', 'Other'].map((lang) => (
                        <label key={lang} className={styles.checkboxCard}>
                          <input
                            type="checkbox"
                            checked={programmingLanguages.includes(lang)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setProgrammingLanguages([...programmingLanguages, lang]);
                              } else {
                                setProgrammingLanguages(programmingLanguages.filter(l => l !== lang));
                              }
                            }}
                          />
                          <span>{lang}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className={styles.formGroup}>
                    <label>
                      <Target size={16} className={styles.labelIcon} />
                      Robotics Background
                    </label>
                    <select
                      value={roboticsBackground}
                      onChange={(e) => setRoboticsBackground(e.target.value)}
                      className={styles.selectInput}
                      required
                    >
                      <option value="">Select your background</option>
                      <option value="none">No robotics experience</option>
                      <option value="courses">Completed robotics courses</option>
                      <option value="projects">Personal/hobby projects</option>
                      <option value="research">Research experience</option>
                      <option value="industry">Industry experience</option>
                    </select>
                  </div>

                  <div className={styles.formGroup}>
                    <label>Learning Goals (Optional)</label>
                    <textarea
                      value={learningGoals}
                      onChange={(e) => setLearningGoals(e.target.value)}
                      placeholder="What do you hope to achieve with this textbook? (e.g., build a robot, learn ROS, etc.)"
                      rows={3}
                      className={styles.textareaInput}
                    />
                  </div>

                  <div className={styles.buttonGroup}>
                    <button
                      type="button"
                      className={styles.backBtn}
                      onClick={() => setSignupStep(1)}
                    >
                      <ArrowRight size={18} style={{ transform: 'rotate(180deg)' }} />
                      Back
                    </button>
                    <button
                      type="submit"
                      className={styles.submitBtn}
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <div className={styles.spinner}></div>
                          Creating Account...
                        </>
                      ) : (
                        <>
                          Create Account
                          <CheckCircle size={18} />
                        </>
                      )}
                    </button>
                  </div>
                </form>
              </>
            )}

            <div className={styles.toggle}>
              <p>
                {mode === 'signin' ? "Don't have an account? " : 'Already have an account? '}
                <button
                  type="button"
                  onClick={() => {
                    setMode(mode === 'signin' ? 'signup' : 'signin');
                    setSignupStep(1);
                    setMessage('');
                  }}
                  className={styles.toggleBtn}
                >
                  {mode === 'signin' ? 'Sign Up' : 'Sign In'}
                </button>
              </p>
            </div>

            {mode === 'signup' && (
              <p className={styles.hint}>
                {signupStep === 1
                  ? 'Create a new account to personalize your learning'
                  : 'Help us personalize your learning experience'}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
