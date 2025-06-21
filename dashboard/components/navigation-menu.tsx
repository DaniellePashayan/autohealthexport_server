import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import ModeToggle from "./theme-toggle";
import Link from "next/link";

const NavbarMenu = () => {
  return (
    <section className="py-4">
      <div className="container mx-auto flex max-w-7xl px-4 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between w-full">
          {/* Centered menu items */}
          <NavigationMenu className="flex-1 flex justify-center">
            <NavigationMenuList className="flex space-x-4">
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <Link href="/overview">Overview</Link>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <Link href="/body-composition">Body Composition</Link>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <Link href="/activity">Activity</Link>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <Link href="/nutrition">Nutrition</Link>
                </NavigationMenuLink>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
          {/* Right-aligned theme toggle */}
          <div className="flex items-center justify-end flex-none ml-4">
            <ModeToggle />
          </div>
        </nav>
      </div>
    </section>
  );
};

export { NavbarMenu };
