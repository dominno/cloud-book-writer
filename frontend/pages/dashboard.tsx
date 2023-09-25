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
    children: ISectionProps[];
  };
  onClick: () => void;
}

const DashboardPage: NextPage = () => {
  const [sections, setSections] = useState<ISectionProps[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [currentSection, setCurrentSection] = useState<number | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchSections = async () => {
      try {
        const response = await getRootSections(currentPage);
        setSections(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchSections();
  }, [currentPage, currentSection]);

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

        <div className="mt-6 w-full">
        {sections.map((section) => (
          <Section key={section.section.id} {...section} onClick={() => handleSectionClick(section.section.id)} />
        ))}
        </div>

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