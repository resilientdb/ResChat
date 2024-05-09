import React from 'react';
import markdownContent from './resource/readme.md';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MarkdownComponent = ({ markdownText }) => {
    return (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {markdownText}
        </ReactMarkdown>
    );
};

export default function About() {
    // 假设 markdownContent 是直接导入的 Markdown 文件内容
    return <MarkdownComponent markdownText={markdownContent} />;
}