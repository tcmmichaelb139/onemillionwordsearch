export interface Database {
	public: {
		Tables: {
			words: {
				Row: {
					id: number;
					found: boolean;
				};
			};
		};
		Views: {
			[_ in never]: never;
		};
		Functions: {
			[_ in never]: never;
		};
		Enums: {
			[_ in never]: never;
		};
	};
}
