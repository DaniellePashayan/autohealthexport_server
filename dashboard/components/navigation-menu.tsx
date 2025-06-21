import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import ModeToggle from "./theme-toggle";
import Link from "next/link";
import { Settings } from "lucide-react";

interface MenuItem {
  title: string;
  url: string;
}

const MenuItems: MenuItem[] = [
  { title: "Overview", url: "/overview" },
  { title: "Body Composition", url: "/body-composition" },
  { title: "Activity", url: "/activity" },
  { title: "Nutrition", url: "/nutrition" },
];

const NavbarMenu = () => {
  return (
    <section className="py-4">
      <div className="container mx-auto flex max-w-7xl px-4 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between w-full">
          {/* Centered menu items */}
          <NavigationMenu className="flex-1 flex justify-center">
            <NavigationMenuList className="flex space-x-4">
              {MenuItems.map((item) => (
                <NavigationMenuItem key={item.title}>
                  <NavigationMenuLink asChild>
                    <Link
                      href={item.url}
                      className={navigationMenuTriggerStyle()}
                    >
                      {item.title}
                    </Link>
                  </NavigationMenuLink>
                </NavigationMenuItem>
              ))}
            </NavigationMenuList>
          </NavigationMenu>
          {/* Right-aligned theme toggle */}
          <div className="flex items-center justify-end flex-none ml-4">
            <Link href="/settings" className={navigationMenuTriggerStyle()}>
              <Settings className="h-5 w-5" />
            </Link>
            <ModeToggle />
          </div>
        </nav>
      </div>
    </section>
  );
};

export { NavbarMenu };
