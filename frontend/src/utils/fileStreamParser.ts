/**
 * Parser for streaming file content from AI responses
 * Detects <file path="..."> tags and routes content appropriately
 */

export interface FileStreamState {
  isInFile: boolean;
  currentFilePath: string | null;
  fileContent: string;
  chatContent: string;
  isInCodeBlock: boolean;
  codeBlockLanguage: string | null;
  pendingFilename: string | null;
}

export class FileStreamParser {
  private state: FileStreamState = {
    isInFile: false,
    currentFilePath: null,
    fileContent: '',
    chatContent: '',
    isInCodeBlock: false,
    codeBlockLanguage: null,
    pendingFilename: null,
  };

  private buffer: string = '';  // Buffer for handling incomplete tags across tokens
  private codeBlockCounter: number = 1;  // Counter for auto-generated filenames

  /**
   * Process a token from the stream
   * Returns updated state and any events to trigger
   */
  processToken(token: string): {
    state: FileStreamState;
    events: Array<{ type: 'file_start' | 'file_content' | 'file_end' | 'chat_content'; data: any }>;
  } {
    const events: Array<{ type: 'file_start' | 'file_content' | 'file_end' | 'chat_content'; data: any }> = [];

    // Add to buffer to handle tags split across tokens
    this.buffer += token;
    let remainingToken = this.buffer;

    // ===== PATTERN 1: File tags (preferred) =====
    const fileOpenMatch = remainingToken.match(/<file\s+path=["']([^"']+)["']\s*>/);
    if (fileOpenMatch) {
      const filePath = fileOpenMatch[1];
      const beforeTag = remainingToken.substring(0, fileOpenMatch.index);
      const afterTag = remainingToken.substring(fileOpenMatch.index! + fileOpenMatch[0].length);

      console.log('[PARSER] Found file opening tag:', filePath);

      if (beforeTag.trim()) {
        this.state.chatContent += beforeTag;
        events.push({ type: 'chat_content', data: beforeTag });
      }

      this.state.isInFile = true;
      this.state.currentFilePath = filePath;
      this.state.fileContent = '';

      events.push({ type: 'file_start', data: { path: filePath } });

      remainingToken = afterTag;
      this.buffer = '';
    }

    const fileCloseMatch = remainingToken.match(/<\/file>/);
    if (fileCloseMatch && this.state.isInFile) {
      const beforeTag = remainingToken.substring(0, fileCloseMatch.index);
      const afterTag = remainingToken.substring(fileCloseMatch.index! + fileCloseMatch[0].length);

      console.log('[PARSER] Found file closing tag');

      if (beforeTag) {
        this.state.fileContent += beforeTag;
        events.push({
          type: 'file_content',
          data: { path: this.state.currentFilePath, content: beforeTag }
        });
      }

      events.push({
        type: 'file_end',
        data: {
          path: this.state.currentFilePath,
          fullContent: this.state.fileContent
        }
      });

      this.state.isInFile = false;
      this.state.currentFilePath = null;
      this.state.fileContent = '';

      remainingToken = afterTag;
      this.buffer = '';

      if (remainingToken.trim()) {
        this.state.chatContent += remainingToken;
        events.push({ type: 'chat_content', data: remainingToken });
      }
    } else if (this.state.isInFile) {
      this.state.fileContent += remainingToken;
      events.push({
        type: 'file_content',
        data: { path: this.state.currentFilePath, content: remainingToken }
      });
      this.buffer = '';
    }

    // ===== PATTERN 2: Markdown code blocks (fallback) =====
    else {
      // Look for filename in the buffer: "Creating `main.py`:" or "Creating `main.py` for..."
      // Make backticks required and allow text after filename
      const filenameMatch = remainingToken.match(/(?:Creating|creating)\s+[`'"]([a-zA-Z0-9_./]+\.[a-zA-Z0-9]+)[`'"]/);
      if (filenameMatch) {
        this.state.pendingFilename = filenameMatch[1];
        console.log('[PARSER] ✓ Found filename:', this.state.pendingFilename, 'in token:', remainingToken.substring(0, 100));
      } else if (remainingToken.includes('Creating') || remainingToken.includes('creating')) {
        console.log('[PARSER] ✗ Creating keyword found but no filename matched in:', remainingToken.substring(0, 100));
      }

      // Check for code block start (``` can be anywhere in token)
      const codeBlockStart = remainingToken.match(/```(\w+)?/);
      if (codeBlockStart && !this.state.isInCodeBlock) {
        const language = codeBlockStart[1] || 'text';
        const matchIndex = codeBlockStart.index!;

        this.state.isInCodeBlock = true;
        this.state.codeBlockLanguage = language;

        // Determine filename
        let filename: string;
        if (this.state.pendingFilename) {
          filename = this.state.pendingFilename;
          this.state.pendingFilename = null;
        } else {
          // Auto-generate filename based on language
          const extMap: Record<string, string> = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'java': 'java',
            'html': 'html',
            'css': 'css',
            'json': 'json',
            'yaml': 'yaml',
            'sql': 'sql',
            'bash': 'sh',
            'sh': 'sh',
          };
          const ext = extMap[language.toLowerCase()] || 'txt';
          filename = `file_${this.codeBlockCounter++}.${ext}`;
        }

        this.state.currentFilePath = filename;
        this.state.fileContent = '';

        console.log('[PARSER] Started code block for:', filename);
        events.push({ type: 'file_start', data: { path: filename } });

        // Everything before the ``` goes to chat (brief status messages)
        const beforeBlock = remainingToken.substring(0, matchIndex);
        if (beforeBlock.trim()) {
          events.push({ type: 'chat_content', data: beforeBlock });
        }

        // Everything after ```language and newline goes to file content
        const afterMarker = remainingToken.substring(matchIndex + codeBlockStart[0].length);
        // Skip the newline after ```python
        let codeStart = afterMarker.replace(/^\n/, '');

        // Check if closing ``` is also in this token
        const closingIndex = codeStart.indexOf('```');
        if (closingIndex !== -1) {
          // Both opening and closing in same token!
          const actualCode = codeStart.substring(0, closingIndex);
          if (actualCode) {
            this.state.fileContent += actualCode;
            events.push({
              type: 'file_content',
              data: { path: filename, content: actualCode }
            });
          }

          // End file immediately
          events.push({
            type: 'file_end',
            data: {
              path: filename,
              fullContent: this.state.fileContent
            }
          });

          console.log('[PARSER] Ended code block for:', filename);

          this.state.isInCodeBlock = false;
          this.state.currentFilePath = null;
          this.state.fileContent = '';

          // Process anything after closing ```
          const afterClosing = codeStart.substring(closingIndex + 3);
          if (afterClosing.trim()) {
            events.push({ type: 'chat_content', data: afterClosing });
          }
        } else {
          // No closing yet, add all content
          if (codeStart) {
            this.state.fileContent += codeStart;
            events.push({
              type: 'file_content',
              data: { path: filename, content: codeStart }
            });
          }
        }

        this.buffer = '';
      }
      // Check for code block end
      else if (this.state.isInCodeBlock) {
        const codeBlockEnd = remainingToken.indexOf('```');
        if (codeBlockEnd !== -1) {
          // Everything before ``` is file content
          const beforeEnd = remainingToken.substring(0, codeBlockEnd);
          if (beforeEnd) {
            this.state.fileContent += beforeEnd;
            events.push({
              type: 'file_content',
              data: { path: this.state.currentFilePath, content: beforeEnd }
            });
          }

          // End file streaming
          events.push({
            type: 'file_end',
            data: {
              path: this.state.currentFilePath,
              fullContent: this.state.fileContent
            }
          });

          console.log('[PARSER] Ended code block for:', this.state.currentFilePath);

          this.state.isInCodeBlock = false;
          this.state.currentFilePath = null;
          this.state.fileContent = '';
          this.state.codeBlockLanguage = null;

          // Everything after ``` goes to chat
          const afterEnd = remainingToken.substring(codeBlockEnd + 3);
          if (afterEnd.trim()) {
            events.push({ type: 'chat_content', data: afterEnd });
          }

          this.buffer = '';
        } else {
          // We're inside code block, add to file content (NOT chat!)
          this.state.fileContent += remainingToken;
          events.push({
            type: 'file_content',
            data: { path: this.state.currentFilePath, content: remainingToken }
          });
          this.buffer = '';
        }
      }
      // Regular chat content (only when NOT in code block)
      else {
        // Check if we might be at the start of a code block marker
        if (remainingToken.endsWith('`') || remainingToken.endsWith('``')) {
          console.log('[PARSER] Buffering possible incomplete code block marker');
          // Keep in buffer
        } else {
          if (remainingToken.trim()) {
            this.state.chatContent += remainingToken;
            events.push({ type: 'chat_content', data: remainingToken });
          }
          this.buffer = '';
        }
      }
    }

    return { state: { ...this.state }, events };
  }

  reset() {
    this.state = {
      isInFile: false,
      currentFilePath: null,
      fileContent: '',
      chatContent: '',
      isInCodeBlock: false,
      codeBlockLanguage: null,
      pendingFilename: null,
    };
    this.buffer = '';
    this.codeBlockCounter = 1;
  }

  getState(): FileStreamState {
    return { ...this.state };
  }
}
