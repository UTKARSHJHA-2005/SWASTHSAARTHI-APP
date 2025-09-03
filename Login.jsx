import React, { useState } from 'react';
import { View, Text, TextInput,Alert, TouchableOpacity, StyleSheet, Dimensions, StatusBar } from 'react-native';
import { Eye, EyeOff, Mail, Lock, AlertCircle } from 'lucide-react-native';
import { auth } from "@react-native-firebase/auth";
import { useNavigation } from "@react-navigation/native";
import { GoogleSignin } from "@react-native-google-signin/google-signin";

GoogleSignin.configure({
    webClientId: "353391451443-e198kulmfj15vpo7ecaoilu8ou7qaifj.apps.googleusercontent.com", 
});

const { width, height } = Dimensions.get('window');

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [emailFocused, setEmailFocused] = useState(false);
    const [passwordFocused, setPasswordFocused] = useState(false);

    const navigation = useNavigation();

    const handleLogin = async () => {
        if (!email || !password) {
            Alert("Email and password are required");
            return;
        }
        if (password.length < 6) {
            AlertCircle("Password must be at least 6 characters long");
            return;
        }
        try {
            const userCredential = await auth().signInWithEmailAndPassword(email, password);
            console.log("Logged in successfully:", userCredential.user);
            navigation.navigate("Home"); 
        } catch (error) {
            console.error("Error logging in:", error.message);
            Alert(error.message);
        }
    };

    const googlesignin = async () => {
        try {
            const { idToken } = await GoogleSignin.signIn();
            const googleCredential = auth.GoogleAuthProvider.credential(idToken);
            const userCredential = await auth().signInWithCredential(googleCredential);
            console.log("Google sign-in successful:", userCredential.user);
            navigation.navigate("Home");
        } catch (error) {
            console.error("Google sign-in error:", error.message);
            Alert(error.message);
        }
    };

    return (
        <View style={styles.container}>
            <View style={styles.loginBox}>
                {/* Header */}
                <View style={styles.header}>
                    <Text style={styles.subtitle}>Sign in to your account</Text>
                </View>
                {/* Email Input */}
                <View style={styles.inputContainer}>
                    <View style={styles.inputWrapper}>
                        <Mail size={20} color={emailFocused ? "#4f46e5" : "#9ca3af"} style={styles.inputIcon}/>
                        <TextInput style={styles.loginInput} placeholder="Email address" placeholderTextColor="#9ca3af" value={email} onChangeText={setEmail} onFocus={() => setEmailFocused(true)}
                         onBlur={() => setEmailFocused(false)} keyboardType="email-address" autoCapitalize="none" autoComplete="email"/>
                    </View>
                </View>
                {/* Password Input */}
                <View style={styles.inputContainer}>
                    <View style={[ styles.inputWrapper,]}>
                        <Lock size={20} color={passwordFocused ? "#4f46e5" : "#9ca3af"} style={styles.inputIcon}/>
                        <TextInput style={[styles.loginInput, styles.passwordInput]} placeholder="Password" placeholderTextColor="#9ca3af"
                         secureTextEntry={!showPassword} value={password} onChangeText={setPassword} onFocus={() => setPasswordFocused(true)}
                         onBlur={() => setPasswordFocused(false)} autoComplete="password"/>
                        <TouchableOpacity style={styles.eyeIcon} onPress={() => setShowPassword(!showPassword)}>
                            {showPassword ? (
                                <EyeOff size={20} color="#9ca3af" />
                            ) : (
                                <Eye size={20} color="#9ca3af" />
                            )}
                        </TouchableOpacity>
                    </View>
                </View>
                {/* Login Button */}
                <TouchableOpacity style={[styles.loginButton, (!email || !password) && styles.loginButtonDisabled]}
                onPress={handleLogin} disabled={!email || !password} activeOpacity={0.8}>
                    <Text style={styles.loginButtonText}>Sign In</Text>
                </TouchableOpacity>
                {/* Divider */}
                <View style={styles.divider}>
                    <View style={styles.dividerLine} />
                    <Text style={styles.dividerText}>or</Text>
                    <View style={styles.dividerLine} />
                </View>
                {/* Social Login Options */}
                <View style={styles.socialContainer}>
                    <TouchableOpacity style={styles.socialButton}  onPress={googlesignin}>
                        <Text style={styles.socialButtonText}>Continue with Google</Text>
                    </TouchableOpacity>
                </View>
                {/* Sign Up Link */}
                <View style={styles.signupContainer}>
                    <Text style={styles.signupText}>Don't have an account? </Text>
                    <TouchableOpacity>
                        <Text style={styles.signupLink}>Sign Up</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 20,
    },
    loginBox: {
        width: Math.min(width - 40, 400),
        backgroundColor: '#ffffff',
        borderRadius: 24,
        padding: 32,
        shadowOffset: {
            width: 0,
            height: 20,
        },
        shadowOpacity: 0.25,
        shadowRadius: 25,
        elevation: 20,
    },
    header: {
        alignItems: 'center',
        marginBottom: 32,
    },
    loginTitle: {
        fontSize: 28,
        fontWeight: '700',
        color: '#1f2937',
        marginBottom: 8,
        textAlign: 'center',
    },
    subtitle: {
        fontSize: 16,
        color: '#6b7280',
        textAlign: 'center',
    },
    inputContainer: {
        marginBottom: 20,
    },
    inputWrapper: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#f9fafb',
        borderRadius: 16,
        borderWidth: 2,
        borderColor: '#e5e7eb',
        paddingHorizontal: 16,
        paddingVertical: 4,
        transition: 'all 0.2s ease',
    },
    inputWrapperFocused: {
        borderColor: '#4f46e5',
        backgroundColor: '#ffffff',
        shadowColor: '#4f46e5',
        shadowOffset: {
            width: 0,
            height: 0,
        },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 4,
    },
    inputIcon: {
        marginRight: 12,
    },
    loginInput: {
        flex: 1,
        fontSize: 16,
        color: '#1f2937',
        paddingVertical: 16,
        fontWeight: '500',
    },
    passwordInput: {
        paddingRight: 40,
    },
    eyeIcon: {
        position: 'absolute',
        right: 16,
        padding: 4,
    },
    forgotPassword: {
        alignSelf: 'flex-end',
        marginBottom: 24,
    },
    forgotPasswordText: {
        color: '#4f46e5',
        fontSize: 14,
        fontWeight: '600',
    },
    loginButton: {
        backgroundColor: '#4f46e5',
        borderRadius: 16,
        paddingVertical: 18,
        alignItems: 'center',
        marginBottom: 24,
        shadowColor: '#4f46e5',
        shadowOffset: {
            width: 0,
            height: 8,
        },
        shadowOpacity: 0.3,
        shadowRadius: 16,
        elevation: 8,
    },
    loginButtonDisabled: {
        backgroundColor: '#d1d5db',
        shadowOpacity: 0,
        elevation: 0,
    },
    loginButtonText: {
        color: '#ffffff',
        fontSize: 18,
        fontWeight: '700',
        letterSpacing: 0.5,
    },
    divider: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 24,
    },
    dividerLine: {
        flex: 1,
        height: 1,
        backgroundColor: '#e5e7eb',
    },
    dividerText: {
        color: '#9ca3af',
        fontSize: 14,
        marginHorizontal: 16,
        fontWeight: '500',
    },
    socialContainer: {
        gap: 12,
        marginBottom: 24,
    },
    socialButton: {
        backgroundColor: '#f3f4f6',
        borderRadius: 16,
        paddingVertical: 16,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#e5e7eb',
    },
    socialButtonSecondary: {
        backgroundColor: '#000000',
    },
    socialButtonText: {
        color: '#374151',
        fontSize: 16,
        fontWeight: '600',
    },
    socialButtonTextSecondary: {
        color: '#ffffff',
    },
    signupContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
    },
    signupText: {
        color: '#6b7280',
        fontSize: 16,
    },
    signupLink: {
        color: '#4f46e5',
        fontSize: 16,
        fontWeight: '700',
    },
});