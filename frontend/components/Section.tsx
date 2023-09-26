
import React from 'react';
import { Button } from '@nextui-org/react';
import axios from 'axios';
import SectionForm from './SectionForm';
import { deleteSection, updateSection } from '../utils/api';

interface ISectionProps {
  section: {
    id: number;
    title: string;
    content: string;
    parent: number | null;
    nested_sections: ISectionProps[];
  };
  onClick: () => void;
}

const Section: React.FC<ISectionProps> = ({ section, onClick }) => {
  const [isEditing, setIsEditing] = React.useState(false);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleDelete = async () => {
    try {
      await deleteSection(section.id);
      // TODO: Remove this section from the parent state
    } catch (error) {
      console.error(error);
    }
  };

  const handleSave = async (title: string, content: string) => {
    try {
      await updateSection(section.id, { title, content });
      setIsEditing(false);
      // TODO: Update this section in the parent state
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="p-4 border rounded mt-4">
      {section ? (
        isEditing ? (
          <SectionForm id={section.id} title={section.title} content={section.content} parent={section.parent} onSave={handleSave} />
        ) : (
          <>
            <h3>{section.title}</h3>
            <p>{section.content}</p>
            <div className="mt-4">
              <Button size="sm" variant="shadow" onClick={handleEdit}>
                Edit
              </Button>
              <Button size="sm" color="danger" onClick={handleDelete} className="ml-2">
                Delete
              </Button>
            </div>
          </>
        )
      ) : null}
  
      {section && section.children.map((child) => (
        <Section key={child.section.id} {...child} />
      ))}
    </div>
    );
};   

export default Section;


