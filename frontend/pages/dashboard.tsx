import React, { useEffect, useState } from 'react';
import { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Button } from '@nextui-org/react';
import Section from '../components/Section';
import SectionForm from '../components/SectionForm';
import { getRootSections } from '../utils/api';

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

const DashboardPage: NextPage = () => {
  const [sections, setSections] = useState<ISectionProps[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [currentSection, setCurrentSection] = useState<number | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchSections = async () => {
      setIsLoading(true);
      try {
        const response = await getRootSections(currentPage);
        setSections(response);
      } catch (error) {
        console.error(error);
      }
      setIsLoading(false);
    };

    fetchSections();
  }, [currentPage, currentSection]);

  useEffect(() => {
    console.log("sections", sections);
    setSections(sections);
  }, [sections]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/');
  };

  const handleSectionClick = (sectionId: number) => {
    setCurrentSection(sectionId);
  };

  const handleNextPage = () => {
    setCurrentPage((prevPage) => prevPage + 1);
  };

  const handlePrevPage = () => {
    setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold">Dashboard</h1>

        <Button size="sm" variant="shadow" className="mt-4" onClick={handleLogout}>
          Logout
        </Button>

        <SectionForm title="" content="" parent={null} onSave={async (title: string, content: string) => {}} />

        {isLoading ? (
      <p>Loading...</p>
        ) : (
          <div className="mt-6 w-full">
            <p>Sections</p>
            {sections && sections.length > 0 ? (
              sections.map((section) => {
                var sec_obj = {section: section};
                console.log("Rendering section:", section.id); // Log each section before it's rendered
                return (
                  <Section 
                    key={section.id},
                    section={
                      id:section.id,
                      title:section.title,
                      content:section.content,
                      parent:section.parent,
                      author:section.author,
                      children:section.nested_sections
                    },
                    onClick={() => handleSectionClick(section.id)} 
                  />
                );
              })
            ) : "None"}
          </div>
        )}

        <Button size="sm" variant="shadow" onClick={handlePrevPage}>
          Previous Page
        </Button>
        <Button size="sm" variant="shadow" onClick={handleNextPage}>
          Next Page
        </Button>
              </div>
    </div>
  );
};

export default DashboardPage;