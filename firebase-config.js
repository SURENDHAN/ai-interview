// Firebase configuration loader
// This script reads from environment variables served by the backend
export async function getFirebaseConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        return config.firebase;
    } catch (error) {
        console.error('Failed to load Firebase config:', error);
        // Fallback to default config (will be replaced by backend)
        return {
            apiKey: "{{FIREBASE_API_KEY}}",
            authDomain: "{{FIREBASE_AUTH_DOMAIN}}",
            projectId: "{{FIREBASE_PROJECT_ID}}",
            storageBucket: "{{FIREBASE_STORAGE_BUCKET}}",
            messagingSenderId: "{{FIREBASE_MESSAGING_SENDER_ID}}",
            appId: "{{FIREBASE_APP_ID}}",
            measurementId: "{{FIREBASE_MEASUREMENT_ID}}"
        };
    }
}
