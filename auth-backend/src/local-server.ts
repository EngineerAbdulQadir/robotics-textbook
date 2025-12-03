/**
 * Simple Local Auth Server with SQLite
 * For local development only. Production uses Render.com backend.
 */
import express, { Request, Response, NextFunction } from "express";
import cors from "cors";
import bcrypt from "bcryptjs";
import crypto from "crypto";
import fs from "fs";
import path from "path";

const uuidv4 = (): string => crypto.randomUUID();

const app = express();
const PORT = process.env.PORT || 3001;

// JSON file-based storage (persists between restarts)
const DATA_FILE = path.join(__dirname, "../local-data.json");

interface User {
  id: string;
  email: string;
  name: string;
  password: string;
  createdAt: string;
}

interface Session {
  id: string;
  userId: string;
  token: string;
  expiresAt: string;
}

interface DataStore {
  users: User[];
  sessions: Session[];
}

function loadData(): DataStore {
  try {
    if (fs.existsSync(DATA_FILE)) {
      return JSON.parse(fs.readFileSync(DATA_FILE, "utf-8"));
    }
  } catch (e) {
    console.log("Creating new data file...");
  }
  // Default with test user
  const data: DataStore = {
    users: [{
      id: uuidv4(),
      email: "test@example.com",
      name: "Test User",
      password: bcrypt.hashSync("Test123!@", 10),
      createdAt: new Date().toISOString(),
    }],
    sessions: []
  };
  saveData(data);
  return data;
}

function saveData(data: DataStore): void {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

const data = loadData();

// Middleware
app.use(express.json());
app.use(cors({
  origin: ["http://localhost:3000", "http://localhost:5173"],
  credentials: true,
}));

// Cookie parser helper
function parseCookies(cookieHeader: string | undefined): Record<string, string> {
  const cookies: Record<string, string> = {};
  if (!cookieHeader) return cookies;
  cookieHeader.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name && value) cookies[name] = value;
  });
  return cookies;
}

// Logging
app.use((req: Request, _res: Response, next: NextFunction) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// Sign Up
app.post("/api/auth/sign-up", async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, password, name } = req.body;

    if (data.users.find(u => u.email === email)) {
      res.status(400).json({ message: "User already exists" });
      return;
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const user: User = {
      id: uuidv4(),
      email,
      name: name || email.split("@")[0],
      password: hashedPassword,
      createdAt: new Date().toISOString(),
    };
    data.users.push(user);

    // Create session
    const session: Session = {
      id: uuidv4(),
      userId: user.id,
      token: uuidv4(),
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    };
    data.sessions.push(session);
    saveData(data);

    res.setHeader("Set-Cookie", `auth_token=${session.token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=604800`);
    res.json({ user: { id: user.id, email: user.email, name: user.name } });
  } catch (error) {
    console.error("Sign up error:", error);
    res.status(500).json({ message: "Internal server error" });
  }
});

// Sign In
app.post("/api/auth/sign-in", async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, password } = req.body;
    const user = data.users.find(u => u.email === email);

    if (!user || !(await bcrypt.compare(password, user.password))) {
      res.status(401).json({ message: "Invalid email or password" });
      return;
    }

    // Create session
    const session: Session = {
      id: uuidv4(),
      userId: user.id,
      token: uuidv4(),
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    };
    data.sessions.push(session);
    saveData(data);

    res.setHeader("Set-Cookie", `auth_token=${session.token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=604800`);
    res.json({ user: { id: user.id, email: user.email, name: user.name } });
  } catch (error) {
    console.error("Sign in error:", error);
    res.status(500).json({ message: "Internal server error" });
  }
});

// Get Session
app.get("/api/auth/session", (req: Request, res: Response): void => {
  const cookies = parseCookies(req.headers.cookie);
  const token = cookies["auth_token"];

  if (!token) {
    res.json({ user: null });
    return;
  }

  const session = data.sessions.find(s => s.token === token);
  if (!session || new Date(session.expiresAt) < new Date()) {
    data.sessions = data.sessions.filter(s => s.token !== token);
    saveData(data);
    res.json({ user: null });
    return;
  }

  const user = data.users.find(u => u.id === session.userId);
  if (!user) {
    res.json({ user: null });
    return;
  }

  res.json({ user: { id: user.id, email: user.email, name: user.name } });
});

// Sign Out
app.post("/api/auth/sign-out", (req: Request, res: Response) => {
  const cookies = parseCookies(req.headers.cookie);
  const token = cookies["auth_token"];

  if (token) {
    data.sessions = data.sessions.filter(s => s.token !== token);
    saveData(data);
  }

  res.setHeader("Set-Cookie", "auth_token=; Path=/; HttpOnly; Max-Age=0");
  res.json({ success: true });
});

// Health check
app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok", mode: "local-dev", timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║       🚀 Local Auth Server (No Database Required)          ║
╠════════════════════════════════════════════════════════════╣
║  URL: http://localhost:${PORT}                               ║
║  Mode: In-Memory (data resets on restart)                  ║
║                                                            ║
║  Test Account:                                             ║
║    Email: test@example.com                                 ║
║    Password: Test123!@                                     ║
╚════════════════════════════════════════════════════════════╝
  `);
});

