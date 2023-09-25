import React, { useState } from 'react';
import { Button, Input, Textarea } from '@nextui-org/react';
import { createSection, updateSection } from '../utils/api';

interface ISectionFormProps {
  id?: number;
  title: string;
  content: string;
  parent: number | null;
  onSave: (title: string, content: string) => Promise<void>;
}

const SectionForm: React.FC<ISectionFormProps> = ({ id, title: initialTitle, content: initialContent, parent, onSave }) => {
  const [title, setTitle] = useState(initialTitle);
  const [content, setContent] = useState(initialContent);
  const API_URL = process.env.API_URL || 'http://127.0.0.1:8000/';

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
  };

  const handleContentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setContent(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (id) {
      try {
        await updateSection(id, {
          title,
          content,
          parent_seection: parent,
          collaborators: []
        });
      } catch (error) {
        console.error(error);
      }
    } else {
      try {
        await createSection({
          title,
          content,
          parent_seection: null,
          root: true,
          collaborators: []
        });
      } catch (error) {
        console.error(error);
      }
    }

    onSave(title, content);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Title</h3>
      <Input
        width="100%"
        value={title}
        onChange={handleTitleChange}
      />

      <h1>Content</h1>
      <Textarea
        width="100%"
        value={content}
        onChange={handleContentChange}
      />

      <Button type="submit" color="primary">
        Save
      </Button>
    </form>
  );
};

export default SectionForm;

