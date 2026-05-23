"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Card } from "@/components/ui/card";
import { DifyClient, type DifyMessage } from "@/lib/dify";

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
  const scrollRef = useRef<HTMLDivElement>(null);
  const clientRef = useRef(new DifyClient());

  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
    }, 50);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSend = useCallback(async () => {
    const text = input.trim();
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
      for await (const event of client.chat(text)) {
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
  }, [input, loading]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => {
    clientRef.current = new DifyClient();
    setMessages([]);
  };

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
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center">
            <div className="text-center text-muted-foreground space-y-2">
              <p className="text-lg">你好！我是宝可梦助手 ⚡</p>
              <p className="text-sm">你可以问我关于宝可梦的各种问题</p>
              <p className="text-xs opacity-60">例如：喷火龙是什么属性？</p>
            </div>
          </div>
        )}
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
                      <div className="rounded-2xl bg-muted px-4 py-2 text-sm whitespace-pre-wrap">
                        {msg.content}
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
          <Button onClick={handleSend} disabled={loading || !input.trim()}>
            {loading ? "..." : "发送"}
          </Button>
        </div>
      </div>
    </div>
  );
}
