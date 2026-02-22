import React, { useState, useRef, useEffect } from "react";// React
import { View, Text, TextInput, TouchableOpacity, Modal, ScrollView, Image, ActivityIndicator, StyleSheet } from "react-native";// React-Native
import axios from "axios"; // Axios
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";// Keyboard
import { launchImageLibrary } from "react-native-image-picker";// Image Picker
import Icon from "react-native-vector-icons/Ionicons";//Icon
import Login from "./Login";

export default function Chat() {
    const [message, setMessage] = useState("");// Message State
    const [chatHistory, setChatHistory] = useState([]);// Chat History State
    const [loading, setLoading] = useState(false);// Loading State
    const [image, setImage] = useState(null);// Image State
    const scrollViewRef = useRef();// Scroll View 

    // Auto scroll to bottom
    useEffect(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
    }, [chatHistory, loading]);

    // Pick image
    const pickImage = async () => {
        const result = await launchImageLibrary({
            mediaType: "photo",
            quality: 0.7,
        });
        if (!result.didCancel && result.assets && result.assets.length > 0) {
            setImage(result.assets[0]);
        }
    };

    // Send image to API
    const handleSendImage = async () => {
        if (!image) return;
        setLoading(true);
        const formData = new FormData();
        formData.append("file", {
            uri: image.uri,
            type: "image/jpeg",
            name: "upload.jpg",
        });
        try {
            const res = await axios.post("http://192.168.1.1:10000/predict/image", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            const predictedDisease = res.data?.predicted_disease || "No prediction available.";
            setChatHistory((prev) => [
                ...prev,
                { type: "user", content: "[Image uploaded]", image: image.uri },
                { type: "bot", content: predictedDisease },
            ]);
        } catch (error) {
            setChatHistory((prev) => [
                ...prev,
                { type: "error", content: "Error processing your image. Please try again." },
            ]);
        } finally {
            setLoading(false);
            setImage(null);
        }
    };

    // Send text message
    const handleSend = async () => {
        if (!message.trim() && !image) return;
        if (image) {
            handleSendImage();
            return;
        }
        setChatHistory((prev) => [...prev, { type: "user", content: message }]);
        setLoading(true);
        const userMessage = message;
        setMessage("");
        try {
            const res = await axios.post("http://192.168.1.8:10000/predict/symptoms/", {
                symptoms: userMessage,
            });
            console.log("RAW RESPONSE:", res.data);
            const responseData = typeof res.data === "string" ? JSON.parse(res.data) : res.data;
            const precautions = Array.isArray(responseData.precautions)
                ? responseData.precautions.join("\n• ")
                : "No precautions provided";
            const formattedResponse = `🩺 Disease: ${responseData.disease || "N/A"}
📜 Description: ${responseData.description || "N/A"}
⚠️ Severity: ${responseData.severity || "N/A"}
✅ Precautions:\n• ${precautions}
🚨 Urgency: ${responseData.urgency || "N/A"}`;
            setChatHistory((prev) => [...prev, { type: "bot", content: formattedResponse }]);
        } catch (error) {
            console.log("CHAT API ERROR:", error.response?.data || error.message);
            setChatHistory((prev) => [
                ...prev,
                { type: "error", content: "Error processing your request. Please try again." },
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            <KeyboardAwareScrollView style={{ flex: 1 }} contentContainerStyle={{ flexGrow: 1 }} enableOnAndroid={true} extraScrollHeight={90}
                keyboardShouldPersistTaps="handled">
                {/* Header */}
                <View style={styles.header}>
                    <Text style={styles.headerTitle}>AI Medical Assistant</Text>
                    <Text style={styles.headerSubtitle}>Your health, powered by AI diagnosis</Text>
                </View>
                {/* Chat Messages */}
                <ScrollView ref={scrollViewRef} style={styles.chatContainer}>
                    {chatHistory.length === 0 && (
                        <View style={styles.welcomeBox}>
                            <Text style={styles.welcomeText}>
                                Welcome! Describe your symptoms or upload an image to begin.
                            </Text>
                        </View>
                    )}
                    {chatHistory.map((msg, index) => (
                        <View key={index} style={[
                            styles.messageContainer,
                            msg.type === "user" ? styles.userAlign : styles.botAlign,
                        ]}>
                            <View style={[styles.messageBubble,
                            msg.type === "user" ? styles.userBubble
                                : msg.type === "error" ? styles.errorBubble
                                    : styles.botBubble,]}>
                                {msg.image && (
                                    <Image source={{ uri: msg.image }} style={styles.uploadedImage} />
                                )}
                                <Text style={styles.messageText}>{msg.content}</Text>
                            </View>
                        </View>
                    ))}
                    <Modal visible={chatHistory.length >= 8} transparent={true} animationType="slide" >
                        <View style={styles.modalOverlay}>
                            <View>
                                <Login />
                            </View>
                        </View>
                    </Modal>
                    {loading && (
                        <View style={styles.loaderBox}>
                            <ActivityIndicator size="small" color="gray" />
                            <Text style={styles.loaderText}>Processing...</Text>
                        </View>
                    )}
                </ScrollView>
                {/* Input Section */}
                <View style={[
                    styles.inputSection,
                    chatHistory.length >= 8 && { opacity: 0.5 } // faded when locked
                ]}>
                    <TextInput value={message} onChangeText={setMessage} placeholder="Describe your symptoms..."
                        style={styles.input}
                        editable={chatHistory.length < 8} // disable typing
                        multiline />
                    <TouchableOpacity onPress={pickImage} style={styles.iconButton} disabled={chatHistory.length >= 8}>
                        <Icon name="image-outline" size={24} color="black" />
                    </TouchableOpacity>
                    {image && (
                        <Image source={{ uri: image.uri }} style={styles.previewImage} />
                    )}
                    <TouchableOpacity onPress={handleSend}
                        disabled={loading || (!message.trim() && !image) || chatHistory.length >= 8}
                        style={[styles.sendButton,
                        loading || (!message.trim() && !image) || chatHistory.length >= 8
                            ? styles.disabledSend
                            : styles.activeSend,]}>
                        <Icon name="send-outline" size={20} color="#10b981" />
                    </TouchableOpacity>
                </View>
            </KeyboardAwareScrollView>
        </View>
    );
}

// Styles
const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#f0f6ff"
    },
    header: {
        backgroundColor: "white",
        padding: 15,
        marginTop: 26,
        borderBottomWidth: 1,
        borderColor: "#ddd",
        alignItems: "center",
    },
    headerTitle: {
        fontSize: 20,
        fontWeight: "bold",
        color: "#2563eb"
    },
    headerSubtitle: {
        fontSize: 12,
        color: "gray"
    },
    chatContainer: {
        flex: 1,
        padding: 10
    },
    welcomeBox: {
        padding: 10,
        backgroundColor: "#dbeafe",
        borderRadius: 10,
        marginVertical: 10,
    },
    welcomeText: {
        color: "#1d4ed8",
        textAlign: "center"
    },
    messageContainer: {
        flexDirection: "row",
        marginVertical: 5,
        width: "100%"
    },
    loginBox: {
        padding: 20,
        backgroundColor: "white",
        borderTopWidth: 1,
        borderColor: "#ddd",
    },
    loginTitle: {
        fontSize: 16,
        fontWeight: "bold",
        marginBottom: 10,
        color: "#2563eb",
        textAlign: "center",
    },
    loginInput: {
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        padding: 10,
        marginBottom: 10,
    },
    loginButton: {
        backgroundColor: "#2563eb",
        padding: 12,
        borderRadius: 8,
        alignItems: "center",
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: "white", // dark background
        justifyContent: "center",
        alignItems: "center",
    },
    // modalBox: {
    //     width: "85%",
    //     backgroundColor: "white",
    //     borderRadius: 12,
    //     padding: 20,
    //     shadowColor: "#000",
    //     shadowOffset: { width: 0, height: 2 },
    //     shadowOpacity: 0.25,
    //     shadowRadius: 4,
    //     elevation: 5,
    // },

    loginButtonText: {
        color: "white",
        fontWeight: "bold",
    },
    userAlign: { justifyContent: "flex-end" },
    botAlign: { justifyContent: "flex-start" },
    messageBubble: {
        padding: 10,
        borderRadius: 12,
        maxWidth: "70%",
    },
    userBubble: {
        backgroundColor: "#27B4F5",
        borderBottomRightRadius: 0
    },
    botBubble: {
        backgroundColor: "#f3f4f6",
        borderBottomLeftRadius: 0
    },
    errorBubble: { backgroundColor: "#fecaca" },
    messageText: { color: "black" },
    uploadedImage: {
        width: 150,
        height: 150,
        borderRadius: 8,
        marginBottom: 5,
    },
    loaderBox: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "#e5e7eb",
        padding: 8,
        borderRadius: 8,
    },
    loaderText: {
        marginLeft: 8,
        color: "gray"
    },
    inputSection: {
        flexDirection: "row",
        alignItems: "center",
        padding: 10,
        backgroundColor: "white",
        borderTopWidth: 1,
        borderColor: "#ddd",
    },
    input: {
        flex: 1,
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        padding: 10,
        maxHeight: 80,
    },
    iconButton: {
        marginHorizontal: 5,
        padding: 6,
        backgroundColor: "#f3f4f6",
        borderRadius: 8,
    },
    previewImage: {
        width: 40,
        height: 40,
        borderRadius: 8,
        marginHorizontal: 5,
    },
    sendButton: {
        padding: 10,
        borderRadius: 8,
    },
    activeSend: { backgroundColor: "#2563eb" },
    disabledSend: { backgroundColor: "gray" },
});