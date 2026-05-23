"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Card } from "@/components/ui/card";
import { DifyClient, type DifyMessage, type DifyAppParams } from "@/lib/dify";

function BotIcon() {
  return (
    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
      P
    </div>
  );
}

function UserIcon() {
  return (
    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-muted text-muted-foreground text-sm font-bold">
      U
    </div>
  );
}

function ToolCallCard({ tool, input, observation }: { tool: string; input: string; observation?: string }) {
  const toolLabel = tool.replace(/_/g, " ").replace(/tool /, "").slice(0, 40);
  return (
    <Card className="my-2 px-3 py-2 text-xs bg-muted/50 border-primary/20">
      <div className="font-mono text-primary mb-1">🔧 {toolLabel}</div>
      {input && <div className="text-muted-foreground mb-1">参数: {input}</div>}
      {observation && (
        <div className="text-muted-foreground truncate" title={observation}>
          结果: {observation.slice(0, 120)}
          {observation.length > 120 ? "..." : ""}
        </div>
      )}
    </Card>
  );
}

export default function Chat() {
  const [messages, setMessages] = useState<DifyMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [params, setParams] = useState<DifyAppParams | null>(null);
  const [variables, setVariables] = useState<Record<string, string>>({});
  const [showSetup, setShowSetup] = useState(true);
  const [initialized, setInitialized] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const clientRef = useRef(new DifyClient());

  // Fetch app parameters on mount
  useEffect(() => {
    clientRef.current.getAppParams().then((p) => {
      setParams(p);
      // Set default values for variables
      const defaults: Record<string, string> = {};
      for (const field of p.user_input_form) {
        defaults[field.variable] = field.default || "";
      }
      setVariables(defaults);
      // If no variable fields, skip setup and show opening
      if (p.user_input_form.length === 0) {
        setShowSetup(false);
        if (p.opening_statement) {
          setMessages([{ role: "assistant", content: p.opening_statement }]);
        }
      }
    }).catch(() => setInitialized(true));
  }, []);

  // Show opening statement after setup is complete
  const completeSetup = useCallback(() => {
    setShowSetup(false);
    setInitialized(true);
    if (params?.opening_statement) {
      // Replace template variables with actual values
      let statement = params.opening_statement;
      for (const [key, value] of Object.entries(variables)) {
        statement = statement.replace(new RegExp(`{{${key}}}`, 'g'), value || key);
      }
      setMessages([{ role: "assistant", content: statement }]);
    }
  }, [params, variables]);

  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
    }, 50);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSend = useCallback(async (overrideText?: string) => {
    const text = (overrideText || input).trim();
    if (!text || loading) return;
    setInput("");

    const userMessage: DifyMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);
    const currentToolCalls: DifyMessage["toolCalls"] = [];
    let answerContent = "";
    const assistantMessage: DifyMessage = { role: "assistant", content: "", toolCalls: currentToolCalls };
    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const client = clientRef.current;
      for await (const event of client.chat(text, variables)) {
        if (event.event === "agent_thought") {
          if (event.tool) {
            const existing = currentToolCalls.find((t) => t.tool === event.tool && !t.observation);
            if (existing) {
              existing.observation = event.observation || "";
            } else {
              currentToolCalls.push({
                tool: event.tool,
                input: event.tool_input || "",
                observation: event.observation || undefined,
              });
            }
            setMessages((prev) => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last.role === "assistant") {
                updated[updated.length - 1] = { ...last, toolCalls: [...currentToolCalls] };
              }
              return updated;
            });
          }
        } else if (event.event === "agent_message" || event.event === "message") {
          if (event.answer) {
            answerContent += event.answer;
            setMessages((prev) => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last.role === "assistant") {
                updated[updated.length - 1] = { ...last, content: answerContent };
              }
              return updated;
            });
          }
        } else if (event.event === "message_end") {
          break;
        }
      }
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : "Unknown error";
      setMessages((prev) => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last.role === "assistant") {
          updated[updated.length - 1] = { ...last, content: answerContent || `请求失败: ${errMsg}` };
        }
        return updated;
      });
    } finally {
      setLoading(false);
    }
  }, [input, loading, variables]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => {
    clientRef.current = new DifyClient();
    setMessages([]);
    setShowSetup(params ? params.user_input_form.length > 0 : true);
    setInitialized(false);
  };

  // Setup form for conversation variables
  if (showSetup && params && params.user_input_form.length > 0) {
    return (
      <div className="flex h-screen flex-col max-w-md mx-auto items-center justify-center p-8">
        <div className="w-full space-y-6">
          <div className="text-center">
            <BotIcon />
            <h2 className="text-lg font-semibold mt-3">开始对话</h2>
            <p className="text-sm text-muted-foreground mt-1">请填写以下信息</p>
          </div>
          <div className="space-y-4">
            {params.user_input_form.map((field) => (
              <div key={field.variable}>
                <label className="text-sm font-medium mb-1 block">
                  {field.label}
                  {field.required && <span className="text-destructive ml-1">*</span>}
                </label>
                {field.type === "text-input" || field.type === "paragraph" ? (
                  <Input
                    value={variables[field.variable] || ""}
                    onChange={(e) => setVariables((v) => ({ ...v, [field.variable]: e.target.value }))}
                    placeholder={`输入${field.label}`}
                  />
                ) : field.type === "select" && field.options ? (
                  <select
                    className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm"
                    value={variables[field.variable] || ""}
                    onChange={(e) => setVariables((v) => ({ ...v, [field.variable]: e.target.value }))}
                  >
                    {field.options.map((opt) => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                ) : null}
              </div>
            ))}
          </div>
          <Button className="w-full" onClick={completeSetup}>
            开始对话
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen flex-col max-w-3xl mx-auto">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b">
        <div className="flex items-center gap-2">
          <BotIcon />
          <div>
            <h1 className="text-base font-semibold">宝可梦助手</h1>
            <p className="text-xs text-muted-foreground">Pokémon Agent</p>
          </div>
        </div>
        <Button variant="outline" size="sm" onClick={handleNewChat}>
          新对话
        </Button>
      </header>

      {/* Messages */}
      <ScrollArea ref={scrollRef} className="flex-1 px-4 py-4">
        <div className="space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
              {msg.role === "user" ? <UserIcon /> : <BotIcon />}
              <div className={`max-w-[80%] ${msg.role === "user" ? "items-end" : "items-start"}`}>
                {msg.role === "user" ? (
                  <div className="rounded-2xl bg-primary text-primary-foreground px-4 py-2 text-sm">
                    {msg.content}
                  </div>
                ) : (
                  <div className="space-y-1">
                    {msg.toolCalls?.map((tc, j) => (
                      <ToolCallCard key={j} {...tc} />
                    ))}
                    {msg.content && (
                      <div className="rounded-2xl bg-muted px-4 py-2 text-sm prose prose-sm dark:prose-invert max-w-none break-words">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                    )}
                    {loading && i === messages.length - 1 && !msg.content && (
                      <div className="flex gap-1 px-4 py-2">
                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.1s]" />
                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.2s]" />
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Suggested questions — show only on the first (opening) message */}
          {params?.suggested_questions && messages.length === 1 && !loading && (
            <div className="flex flex-wrap gap-2 mt-2">
              {params.suggested_questions.map((q, j) => (
                <Button
                  key={j}
                  variant="outline"
                  size="sm"
                  className="text-xs"
                  onClick={() => handleSend(q)}
                >
                  {q}
                </Button>
              ))}
            </div>
          )}

          {/* Empty state */}
          {messages.length === 0 && !showSetup && (
            <div className="flex h-full items-center justify-center pt-20">
              <div className="text-center text-muted-foreground space-y-2">
                <p className="text-lg">你好！我是宝可梦助手 ⚡</p>
                <p className="text-sm">开始提问吧</p>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      <Separator />

      {/* Input */}
      <div className="p-4">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="问关于宝可梦的问题..."
            disabled={loading}
            className="flex-1"
          />
          <Button onClick={() => handleSend()} disabled={loading || !input.trim()}>
            {loading ? "..." : "发送"}
          </Button>
        </div>
      </div>
    </div>
  );
}
